"""FR-04: 음수 입력 거부"""

import pytest

from entity.converter import Converter
from entity.errors import NegativeValueError
from entity.unit_registry import UnitRegistry


def test_negative_value_rejected():
    converter = Converter(UnitRegistry())

    with pytest.raises(NegativeValueError):
        converter.convert("meter", -1)
