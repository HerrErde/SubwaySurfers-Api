import json
import re
import os


def get_uuid():
    with open("settings.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    catalog_locations = data.get("m_CatalogLocations", [])
    first_id = None

    for entry in catalog_locations:
        if isinstance(entry, dict) and "m_InternalId" in entry:
            first_id = entry["m_InternalId"]
            break

    uuid_match = re.search(
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        first_id or "",
    )
    uuid = uuid_match.group(0) if uuid_match else None

    print(f"Extracted UUID: {uuid}")
    return uuid


def get_file_names():
    with open("catalog.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    internal_ids = data.get("m_InternalIds", [])

    file_names = [os.path.basename(path) for path in internal_ids]

    with open("file_names.json", "w", encoding="utf-8") as out:
        json.dump(file_names, out, indent=2)
