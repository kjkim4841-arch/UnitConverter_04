"""NFR-02: Parser/Registry/Converter/Formatter 모듈 분리"""

from pathlib import Path


SRC = Path(__file__).resolve().parents[2] / "src"


def test_srp_module_files_exist():
    required = [
        SRC / "entity" / "length_unit.py",
        SRC / "entity" / "unit_registry.py",
        SRC / "entity" / "converter.py",
        SRC / "boundary" / "input_parser.py",
        SRC / "boundary" / "output_formatter.py",
    ]

    missing = [str(path.relative_to(SRC.parent)) for path in required if not path.is_file()]

    assert not missing, f"missing SRP modules: {', '.join(missing)}"
