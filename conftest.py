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
    for package in ("entity", "boundary", "control"):
        mod = sys.modules.get(package)
        if mod is not None:
            mod_file = getattr(mod, "__file__", "") or ""
            if "src" not in mod_file.replace("\\", "/"):
                for key in list(sys.modules):
                    if key == package or key.startswith(f"{package}."):
                        del sys.modules[key]


class _SrcPackageImportFixer:
    def find_spec(self, fullname, path, target=None):
        if fullname.split(".", 1)[0] in ("entity", "boundary", "control"):
            _fix_path()
        return None


_fix_path()
sys.meta_path.insert(0, _SrcPackageImportFixer())
