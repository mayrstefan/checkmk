#!/usr/bin/env python3
# Copyright (C) 2023 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.graphing.v1 import graphs, metrics, Title

UNIT_PERCENTAGE = metrics.Unit(metrics.DecimalNotation("%"))

metric_nimble_read_latency_01 = metrics.Metric(
    name="nimble_read_latency_01",
    title=Title("Read latency 0-0.1 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_RED,
)
metric_nimble_read_latency_02 = metrics.Metric(
    name="nimble_read_latency_02",
    title=Title("Read latency 0.1-0.2 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_RED,
)
metric_nimble_read_latency_05 = metrics.Metric(
    name="nimble_read_latency_05",
    title=Title("Read latency 0.2-0.5 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_ORANGE,
)
metric_nimble_read_latency_1 = metrics.Metric(
    name="nimble_read_latency_1",
    title=Title("Read latency 0.5-1.0 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_ORANGE,
)
metric_nimble_read_latency_10 = metrics.Metric(
    name="nimble_read_latency_10",
    title=Title("Read latency 5-10 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_YELLOW,
)
metric_nimble_read_latency_100 = metrics.Metric(
    name="nimble_read_latency_100",
    title=Title("Read latency 50-100 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_YELLOW,
)
metric_nimble_read_latency_1000 = metrics.Metric(
    name="nimble_read_latency_1000",
    title=Title("Read latency 500+ ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_GREEN,
)
metric_nimble_read_latency_2 = metrics.Metric(
    name="nimble_read_latency_2",
    title=Title("Read latency 1-2 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_GREEN,
)
metric_nimble_read_latency_20 = metrics.Metric(
    name="nimble_read_latency_20",
    title=Title("Read latency 10-20 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_BLUE,
)
metric_nimble_read_latency_200 = metrics.Metric(
    name="nimble_read_latency_200",
    title=Title("Read latency 100-200 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_BLUE,
)
metric_nimble_read_latency_5 = metrics.Metric(
    name="nimble_read_latency_5",
    title=Title("Read latency 2-5 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_CYAN,
)
metric_nimble_read_latency_50 = metrics.Metric(
    name="nimble_read_latency_50",
    title=Title("Read latency 20-50 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.DARK_CYAN,
)
metric_nimble_read_latency_500 = metrics.Metric(
    name="nimble_read_latency_500",
    title=Title("Read latency 200-500 ms"),
    unit=UNIT_PERCENTAGE,
    color=metrics.Color.LIGHT_PURPLE,
)

graph_read_latency = graphs.Graph(
    name="read_latency",
    title=Title("Percentage of read I/O operations per latency range"),
    simple_lines=[
        "nimble_read_latency_01",
        "nimble_read_latency_02",
        "nimble_read_latency_05",
        "nimble_read_latency_1",
        "nimble_read_latency_2",
        "nimble_read_latency_5",
        "nimble_read_latency_10",
        "nimble_read_latency_20",
        "nimble_read_latency_50",
        "nimble_read_latency_100",
        "nimble_read_latency_200",
        "nimble_read_latency_500",
        "nimble_read_latency_1000",
    ],
)
