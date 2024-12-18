#!/usr/bin/env python3
# Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from dataclasses import asdict, dataclass, field
from typing import Any, cast

from cmk.ccc.exceptions import MKGeneralException

from cmk.gui.form_specs.vue.form_spec_visitor import (
    parse_value_from_frontend,
    serialize_data_for_frontend,
    validate_value_from_frontend,
)
from cmk.gui.form_specs.vue.visitors import DEFAULT_VALUE
from cmk.gui.form_specs.vue.visitors._type_defs import DataOrigin
from cmk.gui.quick_setup.private.widgets import ConditionalNotificationStageWidget
from cmk.gui.quick_setup.v0_unstable.definitions import QuickSetupSaveRedirect
from cmk.gui.quick_setup.v0_unstable.predefined import (
    build_quick_setup_formspec_map,
    stage_components,
)
from cmk.gui.quick_setup.v0_unstable.setups import (
    QuickSetup,
    QuickSetupAction,
    QuickSetupActionMode,
)
from cmk.gui.quick_setup.v0_unstable.type_defs import (
    GeneralStageErrors,
    ParsedFormData,
    QuickSetupId,
    RawFormData,
    StageIndex,
)
from cmk.gui.quick_setup.v0_unstable.widgets import (
    Collapsible,
    FormSpecId,
    FormSpecWrapper,
    ListOfWidgets,
    Widget,
)

from cmk.rulesets.v1.form_specs import FormSpec


class InvalidStageException(MKGeneralException):
    pass


# TODO: This dataclass is already defined in
# cmk.gui.form_specs.vue.autogen_type_defs.vue_formspec_components
# but can't be imported here. Once we move this module, we can remove this
# and use the one from the other module.
@dataclass
class QuickSetupValidationError:
    message: str
    invalid_value: Any
    location: Sequence[str] = field(default_factory=list)


ValidationErrorMap = MutableMapping[FormSpecId, MutableSequence[QuickSetupValidationError]]


@dataclass
class StageOverview:
    title: str
    sub_title: str | None


@dataclass
class Errors:
    formspec_errors: ValidationErrorMap = field(default_factory=dict)
    stage_errors: GeneralStageErrors = field(default_factory=list)

    def exist(self) -> bool:
        return bool(self.formspec_errors or self.stage_errors)


@dataclass
class NextStageStructure:
    components: Sequence[dict]
    button_label: str | None


@dataclass
class Stage:
    next_stage_structure: NextStageStructure | None = None
    errors: Errors | None = None
    stage_recap: Sequence[Widget] = field(default_factory=list)


@dataclass
class AllStageErrors:
    all_stage_errors: Sequence[Errors]


@dataclass
class CompleteButton:
    id: str
    label: str


@dataclass
class QuickSetupOverview:
    quick_setup_id: QuickSetupId
    overviews: list[StageOverview]
    stage: Stage
    complete_buttons: list[CompleteButton]
    mode: str = field(default="guided")


@dataclass
class CompleteStage:
    title: str
    sub_title: str | None
    components: Sequence[dict]
    button_label: str | None


@dataclass
class QuickSetupAllStages:
    quick_setup_id: QuickSetupId
    stages: list[CompleteStage]
    complete_buttons: list[CompleteButton]
    mode: str = field(default="overview")


def _get_stage_components_from_widget(widget: Widget, prefill_data: ParsedFormData | None) -> dict:
    if isinstance(widget, (ListOfWidgets, Collapsible, ConditionalNotificationStageWidget)):
        widget_as_dict = asdict(widget)
        widget_as_dict["items"] = [
            _get_stage_components_from_widget(item, prefill_data) for item in widget.items
        ]
        return widget_as_dict

    if isinstance(widget, FormSpecWrapper):
        form_spec = cast(FormSpec, widget.form_spec)
        return {
            "widget_type": widget.widget_type,
            "form_spec": asdict(
                serialize_data_for_frontend(
                    form_spec=form_spec,
                    field_id=str(widget.id),
                    origin=DataOrigin.DISK,
                    value=prefill_data.get(widget.id) if prefill_data else DEFAULT_VALUE,
                    do_validate=False,
                )
            ),
        }

    return asdict(widget)


def _stage_validate_all_form_spec_keys_existing(
    current_stage_form_data: RawFormData,
    expected_formspecs_map: Mapping[FormSpecId, FormSpec],
) -> GeneralStageErrors:
    return [
        f"Formspec id '{form_spec_id}' not found"
        for form_spec_id in current_stage_form_data.keys()
        if form_spec_id not in expected_formspecs_map
    ]


def _form_spec_validate(
    current_stage_form_data: RawFormData,
    expected_formspecs_map: Mapping[FormSpecId, FormSpec],
) -> ValidationErrorMap:
    return {
        form_spec_id: [QuickSetupValidationError(**asdict(error)) for error in errors]
        for form_spec_id, form_data in current_stage_form_data.items()
        if (errors := validate_value_from_frontend(expected_formspecs_map[form_spec_id], form_data))
    }


def _form_spec_parse(
    all_stages_form_data: Sequence[RawFormData],
    expected_formspecs_map: Mapping[FormSpecId, FormSpec],
) -> ParsedFormData:
    return {
        form_spec_id: parse_value_from_frontend(expected_formspecs_map[form_spec_id], form_data)
        for current_stage_form_data in all_stages_form_data
        for form_spec_id, form_data in current_stage_form_data.items()
    }


def quick_setup_guided_mode(
    quick_setup: QuickSetup, prefill_data: ParsedFormData | None
) -> QuickSetupOverview:
    stages = [stage() for stage in quick_setup.stages]
    return QuickSetupOverview(
        quick_setup_id=quick_setup.id,
        overviews=[
            StageOverview(
                title=stage.title,
                sub_title=stage.sub_title,
            )
            for stage in stages
        ],
        stage=Stage(
            next_stage_structure=NextStageStructure(
                components=[
                    _get_stage_components_from_widget(widget, prefill_data)
                    for widget in stage_components(stages[0])
                ],
                button_label=stages[0].button_label,
            ),
        ),
        complete_buttons=[
            CompleteButton(id=action.id, label=action.label) for action in quick_setup.actions
        ],
    )


def validate_stage(
    quick_setup: QuickSetup,
    stages_raw_formspecs: Sequence[RawFormData],
    stage_index: StageIndex,
) -> Errors | None:
    errors = Errors()
    stages = [stage() for stage in quick_setup.stages]
    quick_setup_formspec_map = build_quick_setup_formspec_map(stages)

    errors.stage_errors.extend(
        _stage_validate_all_form_spec_keys_existing(
            stages_raw_formspecs[-1], quick_setup_formspec_map
        )
    )
    if errors.exist():
        return errors

    errors.formspec_errors = _form_spec_validate(
        stages_raw_formspecs[-1],
        quick_setup_formspec_map,
    )
    if errors.exist():
        return errors

    for custom_validator in stages[stage_index].custom_validators:
        errors.stage_errors.extend(
            custom_validator(
                quick_setup.id,
                StageIndex(len(stages_raw_formspecs) - 1),
                _form_spec_parse(stages_raw_formspecs, quick_setup_formspec_map),
            )
        )
    return errors if errors.exist() else None


def validate_stages(
    quick_setup: QuickSetup,
    stages_raw_formspecs: Sequence[RawFormData],
) -> Sequence[Errors] | None:
    return [
        errors
        for stage_index, raw_formspec in enumerate(stages_raw_formspecs)
        if (errors := validate_stage(quick_setup, [raw_formspec], StageIndex(stage_index)))
    ] or None


def retrieve_next_stage(
    quick_setup: QuickSetup,
    stages_raw_formspecs: Sequence[RawFormData],
    prefill_data: ParsedFormData | None = None,
) -> Stage:
    current_stage_index = StageIndex(len(stages_raw_formspecs) - 1)
    stages = [stage() for stage in quick_setup.stages]
    quick_setup_formspec_map = build_quick_setup_formspec_map(stages)

    current_stage_recap = [
        r
        for recap_callable in stages[current_stage_index].recap
        for r in recap_callable(
            quick_setup.id,
            current_stage_index,
            _form_spec_parse(stages_raw_formspecs, quick_setup_formspec_map),
        )
    ]

    if current_stage_index == len(quick_setup.stages) - 1:
        return Stage(next_stage_structure=None, stage_recap=current_stage_recap)

    next_stage = stages[current_stage_index + 1]

    return Stage(
        next_stage_structure=NextStageStructure(
            components=[
                _get_stage_components_from_widget(widget, prefill_data)
                for widget in stage_components(next_stage)
            ],
            button_label=next_stage.button_label,
        ),
        stage_recap=current_stage_recap,
    )


def complete_quick_setup(
    quick_setup: QuickSetup,
    action: QuickSetupAction,
    mode: QuickSetupActionMode,
    stages_raw_formspecs: Sequence[RawFormData],
    object_id: str | None = None,
) -> QuickSetupSaveRedirect:
    return QuickSetupSaveRedirect(
        redirect_url=action.action(
            _form_spec_parse(
                stages_raw_formspecs,
                build_quick_setup_formspec_map([stage() for stage in quick_setup.stages]),
            ),
            mode,
            object_id,
        )
    )


def quick_setup_overview_mode(
    quick_setup: QuickSetup, prefill_data: ParsedFormData | None
) -> QuickSetupAllStages:
    stages = [stage() for stage in quick_setup.stages]
    return QuickSetupAllStages(
        quick_setup_id=quick_setup.id,
        stages=[
            CompleteStage(
                title=stage.title,
                sub_title=stage.sub_title,
                components=[
                    _get_stage_components_from_widget(widget, prefill_data)
                    for widget in stage_components(stage)
                ],
                button_label=stage.button_label,
            )
            for stage in stages
        ],
        complete_buttons=[
            CompleteButton(id=action.id, label=action.label) for action in quick_setup.actions
        ],
    )
