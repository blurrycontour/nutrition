import os
from pathlib import Path

SETTINGS_FILE = os.getenv("NUTRITION_CONFIG", Path.home() / ".nutcfg.yaml")
