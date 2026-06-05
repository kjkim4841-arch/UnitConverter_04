import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = str(ROOT / "src")
TESTS = str(ROOT / "tests")


def _fix_path() -> None:
    while TESTS in sys.path:
        sys.path.remove(TESTS)
    if SRC in sys.path:
        sys.path.remove(SRC)
    sys.path.insert(0, SRC)
    entity = sys.modules.get("entity")
    if entity is not None:
        entity_file = getattr(entity, "__file__", "") or ""
        if "src" not in entity_file.replace("\\", "/"):
            for key in list(sys.modules):
                if key == "entity" or key.startswith("entity."):
                    del sys.modules[key]


class _EntityImportFixer:
    def find_spec(self, fullname, path, target=None):
        if fullname == "entity" or fullname.startswith("entity."):
            _fix_path()
        return None


_fix_path()
sys.meta_path.insert(0, _EntityImportFixer())
