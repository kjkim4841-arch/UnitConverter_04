from typing import Protocol

METERS_PER_FOOT = 3.28084
METERS_PER_YARD = 1.09361


class LengthUnit(Protocol):
    name: str

    def to_meter(self, value: float) -> float: ...


class _RatioBasedUnit:
    def __init__(self, name: str, meters_per_unit: float) -> None:
        self.name = name
        self._meters_per_unit = meters_per_unit

    def to_meter(self, value: float) -> float:
        return value / self._meters_per_unit


class MeterUnit:
    name = "meter"

    def to_meter(self, value: float) -> float:
        return value


class FeetUnit(_RatioBasedUnit):
    def __init__(self) -> None:
        super().__init__("feet", METERS_PER_FOOT)


class YardUnit(_RatioBasedUnit):
    def __init__(self) -> None:
        super().__init__("yard", METERS_PER_YARD)
