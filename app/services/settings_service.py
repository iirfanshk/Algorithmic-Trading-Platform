import json
from pathlib import Path

SETTINGS_FILE = Path("settings.json")


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

    return True


def load_settings():

    if SETTINGS_FILE.exists():

        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)

    return {
        "theme": "Dark",
        "capital": 10000,
        "commission": 0.10,
        "slippage": 0.05,
        "stoploss": 5,
        "takeprofit": 10
    }