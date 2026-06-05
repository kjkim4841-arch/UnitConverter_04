"""FR-05: 잘못된 형식 오류"""

import pytest

from boundary.input_parser import InputParser
from entity.errors import InvalidFormatError


@pytest.mark.parametrize(
    "raw_input",
    [
        "meter",
        "meter:abc",
        "meter:2.5:extra",
        ":2.5",
        "meter:",
    ],
)
def test_invalid_format_rejected(raw_input):
    parser = InputParser()

    with pytest.raises(InvalidFormatError):
        parser.parse(raw_input)
