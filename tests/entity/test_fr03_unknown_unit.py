"""FR-03: 미지 단위 오류"""

import pytest

from entity.converter import Converter
from entity.errors import UnknownUnitError
from entity.unit_registry import UnitRegistry


def test_unknown_unit_rejected():
    converter = Converter(UnitRegistry())

    with pytest.raises(UnknownUnitError):
        converter.convert("cubit", 1)
