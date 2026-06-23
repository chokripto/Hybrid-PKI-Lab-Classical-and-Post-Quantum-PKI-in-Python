import os
import sys
from pathlib import Path

os.environ.setdefault("HYBRID_PKI_DISABLE_OQS", "1")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

for path in [PROJECT_ROOT, SRC_DIR]:
    path_as_string = str(path)

    if path_as_string not in sys.path:
        sys.path.insert(0, path_as_string)
