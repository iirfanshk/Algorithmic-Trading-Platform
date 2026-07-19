import pandas as pd
import joblib
from pathlib import Path


def get_saved_models():

    models_dir = Path("models")

    if not models_dir.exists():
        return []

    return sorted(

        [f.name for f in models_dir.glob("*.pkl")]

    )