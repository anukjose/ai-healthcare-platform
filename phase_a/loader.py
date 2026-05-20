import json
from pathlib import Path


def load_patient_json(file_path: str) -> dict:
    """
    Load patient JSON file safely.

    Args:
        file_path (str): path to JSON file

    Returns:
        dict: parsed patient data
    """

    path = Path(file_path)

    # Check file exists
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"✅ Loaded patient JSON from {file_path}")

        return data

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

    except Exception as e:
        raise RuntimeError(f"Unexpected error while loading JSON: {e}")