from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
__path__ = [str(_SRC / "dodo")]
sys.path.insert(0, str(_SRC))

from dodo.cli import app


if __name__ == "__main__":
    app()
