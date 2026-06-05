from dataclasses import dataclass

from entity.errors import InvalidFormatError


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: float


def _reject_invalid_format(raw: str) -> None:
    raise InvalidFormatError(f"Invalid format: {raw!r}")


class InputParser:
    def parse(self, raw: str) -> ParsedInput:
        trimmed = raw.strip()
        if ":" not in trimmed:
            _reject_invalid_format(raw)
        unit_part, value_part = trimmed.split(":", 1)
        unit = unit_part.strip()
        value_str = value_part.strip()
        if not unit or not value_str:
            _reject_invalid_format(raw)
        try:
            value = float(value_str)
        except ValueError as exc:
            raise InvalidFormatError(f"Invalid format: {raw!r}") from exc
        return ParsedInput(unit=unit, value=value)
