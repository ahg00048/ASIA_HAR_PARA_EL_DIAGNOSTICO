import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    _BASE = Path(sys._MEIPASS)
else:
    _BASE = Path(__file__).resolve().parent.parent  

RESOURCES_DIR = _BASE / "ui" / "resources/"