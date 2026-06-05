"""FR-01: unit:value 파싱"""

from boundary.input_parser import InputParser


def test_parse_meter_value():
    parser = InputParser()

    result = parser.parse("meter:2.5")

    assert result.unit == "meter"
    assert result.value == 2.5


def test_parse_trims_whitespace():
    parser = InputParser()

    result = parser.parse(" meter : 2.5 ")

    assert result.unit == "meter"
    assert result.value == 2.5
