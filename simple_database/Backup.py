import json


def backup_to_json(data: dict, backup_file: str):
    with open(backup_file, "w") as f:
        json.dump(data, f)


def restore_from_json(backup_file: str) -> dict:
    with open(backup_file, "r") as f:
        return json.load(f)
