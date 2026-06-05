from typing import Protocol


class LengthUnit(Protocol):
    name: str

    def to_meter(self, value: float) -> float: ...


class MeterUnit:
    name = "meter"

    def to_meter(self, value: float) -> float:
        return value


class FeetUnit:
    name = "feet"

    def to_meter(self, value: float) -> float:
        return value / 3.28084


class YardUnit:
    name = "yard"

    def to_meter(self, value: float) -> float:
        return value / 1.09361
