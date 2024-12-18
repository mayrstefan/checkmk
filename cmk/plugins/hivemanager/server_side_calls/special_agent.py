#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterable

from pydantic import BaseModel

from cmk.server_side_calls.v1 import HostConfig, Secret, SpecialAgentCommand, SpecialAgentConfig


class _Params(BaseModel, frozen=True):
    username: str
    password: Secret


def _commands_function(
    params: _Params,
    host_config: HostConfig,
) -> Iterable[SpecialAgentCommand]:
    yield SpecialAgentCommand(
        command_arguments=[
            host_config.primary_ip_config.address,
            params.username,
            params.password.unsafe(),
            "--cert-server-name",
            host_config.name,
        ]
    )


special_agent_hivemanager = SpecialAgentConfig(
    name="hivemanager",
    parameter_parser=_Params.model_validate,
    commands_function=_commands_function,
)
