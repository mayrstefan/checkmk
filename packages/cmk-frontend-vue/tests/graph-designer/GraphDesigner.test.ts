/**
 * Copyright (C) 2024 Checkmk GmbH - License: GNU General Public License v2
 * This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
 * conditions defined in the file COPYING, which is part of this source code package.
 */
import { render } from '@testing-library/vue'
import GraphDesignerApp from '@/graph-designer/GraphDesignerApp.vue'

test('Render GraphDesignerApp', () => {
  render(GraphDesignerApp, {
    props: {
      i18n: {
        graph_options: {
          unit_first_with_unit: 'unit_first_with_unit',
          unit_custom: 'unit_custom',
          unit_custom_notation: 'unit_custom_notation',
          unit_custom_notation_symbol: 'unit_custom_notation_symbol',
          unit_custom_notation_decimal: 'unit_custom_notation_decimal',
          unit_custom_notation_si: 'unit_custom_notation_si',
          unit_custom_notation_iec: 'unit_custom_notation_iec',
          unit_custom_notation_standard_scientific: 'unit_custom_notation_standard_scientific',
          unit_custom_notation_engineering_scientific:
            'unit_custom_notation_engineering_scientific',
          unit_custom_notation_time: 'unit_custom_notation_time',
          unit_custom_precision: 'unit_custom_precision',
          unit_custom_precision_rounding_mode: 'unit_custom_precision_rounding_mode',
          unit_custom_precision_rounding_mode_auto: 'unit_custom_precision_rounding_mode_auto',
          unit_custom_precision_rounding_mode_strict: 'unit_custom_precision_rounding_mode_strict',
          unit_custom_precision_digits: 'unit_custom_precision_digits',
          vertical_range_auto: 'vertical_range_auto',
          vertical_range_explicit: 'vertical_range_explicit',
          vertical_range_explicit_lower: 'vertical_range_explicit_lower',
          vertical_range_explicit_upper: 'vertical_range_explicit_upper'
        },
        topics: {
          metric: 'metric',
          scalar: 'scalar',
          constant: 'constant',
          graph_lines: 'graph_lines',
          operations: 'operations',
          transformation: 'transformation',
          graph_operations: 'graph_operations',
          unit: 'unit',
          vertical_range: 'vertical_range',
          metrics_with_zero_values: 'metrics_with_zero_values',
          graph_options: 'graph_options'
        }
      }
    }
  })
})
