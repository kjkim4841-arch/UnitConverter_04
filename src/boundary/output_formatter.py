class OutputFormatter:
    def format(self, source_value: float, source_unit: str, results: dict[str, float]) -> str:
        lines = [
            f"{source_value} {source_unit} = {value:.4f} {unit}"
            for unit, value in results.items()
        ]
        return "\n".join(lines)
