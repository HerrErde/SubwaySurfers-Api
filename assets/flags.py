import json
import re


def get_country_codes():
    with open("catalog.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    internal_ids = data.get("m_InternalIds", [])

    pattern = re.compile(r"countryflags-builtin_assets_([a-z]{2})_", re.IGNORECASE)

    codes = set()

    for path in internal_ids:
        match = pattern.search(path)
        if match:
            codes.add(match.group(1).lower())

    with open("country_iso.txt", "w", encoding="utf-8") as out:
        for code in sorted(codes):
            out.write(code + "\n")

    with open("country_iso.json", "w", encoding="utf-8") as out:
        json.dump(sorted(codes), out, indent=2)


get_country_codes()
