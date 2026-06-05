from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float


class InputParser:
    def parse(self, raw: str) -> ParsedInput:
        unit_part, value_part = raw.strip().split(":", 1)
        return ParsedInput(unit=unit_part.strip(), value=float(value_part.strip()))
