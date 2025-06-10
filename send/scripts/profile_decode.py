import ast
import json


def recursive_json_decode(obj):
    # Recursively decode JSON strings within dicts/lists.
    if isinstance(obj, dict):
        return {k: recursive_json_decode(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_json_decode(i) for i in obj]
    elif isinstance(obj, str):
        try:
            return recursive_json_decode(json.loads(obj))
        except json.JSONDecodeError:
            return obj
    else:
        return obj


with open("input.json", "r", encoding="utf-8") as f:
    raw = f.read()

data = ast.literal_eval(raw)

fixed_data = recursive_json_decode(data)

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(fixed_data, f, indent=2)
