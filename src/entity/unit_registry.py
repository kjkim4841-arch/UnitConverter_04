from entity.length_unit import FeetUnit, LengthUnit, MeterUnit, YardUnit


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, LengthUnit] = {}
        for unit in (MeterUnit(), FeetUnit(), YardUnit()):
            self.register(unit)

    def register(self, unit: LengthUnit) -> None:
        self._units[unit.name] = unit

    def get(self, name: str) -> LengthUnit:
        return self._units[name]

    def all_units(self) -> list[LengthUnit]:
        return list(self._units.values())
