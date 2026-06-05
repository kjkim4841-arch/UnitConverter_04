"""FR-02: 전 단위 출력"""

import pytest

from entity.converter import Converter
from entity.unit_registry import UnitRegistry


def test_meter_converts_to_all_registered_units():
    registry = UnitRegistry()
    converter = Converter(registry)

    results = converter.convert("meter", 2.5)

    assert results["feet"] == pytest.approx(8.2021, rel=1e-4)
    assert results["yard"] == pytest.approx(2.7340, rel=1e-4)
