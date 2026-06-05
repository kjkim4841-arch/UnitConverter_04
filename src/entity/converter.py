from entity.errors import NegativeValueError
from entity.length_unit import LengthUnit
from entity.unit_registry import UnitRegistry


class Converter:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert(self, source_name: str, value: float) -> dict[str, float]:
        if value < 0:
            raise NegativeValueError(f"Negative value not allowed: {value}")
        source = self._registry.get(source_name)
        meter_value = source.to_meter(value)
        return {
            unit.name: _from_meter(unit, meter_value)
            for unit in self._registry.all_units()
            if unit.name != source_name
        }


def _from_meter(unit: LengthUnit, meter_value: float) -> float:
    return meter_value / unit.to_meter(1.0)
