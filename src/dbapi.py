import json
import os

file_path = "alts_map.json"

def set_alts(user_id: str, alts: list[str]):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)
    with open(file_path, 'r') as f:
        data = json.load(f)
    data[user_id] = alts
    with open('alts_map.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_alts(user_id: str) -> list[str] | None:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data[user_id] if user_id in data else None


