"""NFR-01: OCP — inch 추가 시 converter 핵심 미수정"""

from entity.converter import Converter
from entity.unit_registry import UnitRegistry


class InchUnit:
    name = "inch"

    def to_meter(self, value: float) -> float:
        return value * 0.0254


def test_register_inch_without_modifying_converter():
    registry = UnitRegistry()
    registry.register(InchUnit())
    converter = Converter(registry)

    results = converter.convert("meter", 1.0)

    assert "inch" in results
