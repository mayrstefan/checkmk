<!--
Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
conditions defined in the file COPYING, which is part of this source code package.
-->
<script setup lang="ts">
// TODO: move this file CMK-19774
import { ref } from 'vue'
import type { CheckboxListChoice } from 'cmk-shared-typing/typescript/vue_formspec_components'
import FormCheckboxListChoice, {
  type CheckboxListChoiceElement
} from '@/form/components/forms/FormCheckboxListChoice.vue'

defineProps<{ screenshotMode: boolean }>()

const spec: CheckboxListChoice = {
  type: 'checkbox_list_choice',
  title: 'some title',
  help: 'some help',
  validators: [],
  elements: [
    {
      name: 'some_name_1',
      title: 'some title 1'
    },
    {
      name: 'some_name_2',
      title: 'some title 2'
    }
  ],
  i18n: {
    add: 'i18n add',
    remove: 'i18n remove',
    add_all: 'i18n add_all',
    remove_all: 'i18n remove_all',
    available_options: 'i18n available_options',
    selected_options: 'i18n selected_options',
    selected: 'i18n selected',
    no_elements_available: 'i18n no_elements_available',
    no_elements_selected: 'i18n no_elements_selected',
    search_selected_options: 'i18n search selected options',
    search_available_options: 'i18n search available options',
    autocompleter_loading: 'i18n autocompleter_loading',
    and_x_more: 'i18n and_x_more'
  }
}

const data = ref<Array<CheckboxListChoiceElement>>([
  {
    name: 'some_name_1',
    title: 'some title 1'
  }
])
</script>

<template>
  <pre>{{ JSON.stringify(data) }}</pre>
  <FormCheckboxListChoice v-model:data="data" :spec="spec" :backend-validation="[]" />
</template>
