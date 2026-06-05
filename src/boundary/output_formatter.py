OUTPUT_DECIMAL_PLACES = 4


class OutputFormatter:
    def format(self, source_value: float, source_unit: str, results: dict[str, float]) -> str:
        lines = [
            f"{source_value} {source_unit} = {value:.{OUTPUT_DECIMAL_PLACES}f} {unit}"
            for unit, value in results.items()
        ]
        return "\n".join(lines)
