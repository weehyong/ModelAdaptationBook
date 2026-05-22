"""Pytest configuration. Ensures code/ is on sys.path so chapter05 and common are importable."""
from __future__ import annotations

import sys
from pathlib import Path

# When running pytest from code/, make the code root (parent of tests/) on path
# so that "import chapter05" and "import common" work without pip install -e .
_code_root = Path(__file__).resolve().parent.parent
if str(_code_root) not in sys.path:
    sys.path.insert(0, str(_code_root))
