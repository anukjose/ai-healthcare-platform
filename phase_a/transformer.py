from typing import List, Dict


# Unit normalization map
UNIT_MAP = {
    "mg%": "mg/dL",
    "mg/dl": "mg/dL",
    "gm/dL": "g/dL",
    "gms%": "g/dL",
    "gm%": "g/dL",
    "fl": "fL"
}


def normalize_unit(unit: str) -> str:

    if not unit:
        return ""

    unit = unit.strip()

    return UNIT_MAP.get(unit, unit)


def transform_labs(data: dict) -> List[Dict]:

    transformed_labs = []

    patient_id = data.get("patient_id", "UNKNOWN")

    labs = data.get("labs", [])

    for lab in labs:

        # Skip invalid rows
        if not lab.get("test"):
            continue

        if not lab.get("date"):
            continue

        if lab.get("value") is None:
            continue

        transformed_lab = {
            "patient_id": patient_id,
            "test": lab.get("test"),
            "date": lab.get("date"),
            "value": lab.get("value"),
            "unit": normalize_unit(lab.get("unit", ""))
        }

        transformed_labs.append(transformed_lab)

    print(f"✅ Transformed {len(transformed_labs)} lab records")

    return transformed_labs