"""Update strings.json and en.json from const.py."""
import json
import sys
from pathlib import Path

import yaml

sys.path.append(str(Path(__file__).parent.parent))

from custom_components.adaptive_lighting import const  # noqa: E402

folder = Path("custom_components") / "adaptive_lighting"
strings_fname = folder / "strings.json"
en_fname = folder / "translations" / "en.json"
with strings_fname.open() as f:
    strings = json.load(f)

# Set "options"
data = {k: f"{k}: {const.DOCS[k]}" for k, _, _ in const.VALIDATION_TUPLES}
strings["options"]["step"]["init"]["data"] = data

# Set "services"
services_filename = Path("custom_components") / "adaptive_lighting" / "services.yaml"
with open(services_filename) as f:  # noqa: PTH123
    services = yaml.safe_load(f)
services_json = {}
for service_name, dct in services.items():
    services_json[service_name] = {
        "name": service_name,
        "description": dct["description"],
        "fields": {},
    }
    for field_name, field in dct["fields"].items():
        services_json[service_name]["fields"][field_name] = {
            "description": field["description"],
            "name": field_name,
        }
strings["services"] = services_json

# Write changes to strings.json
with strings_fname.open("w") as f:
    json.dump(strings, f, indent=2, ensure_ascii=False)
    f.write("\n")

# Sync changes from strings.json to en.json
with en_fname.open() as f:
    en = json.load(f)

en["config"]["step"]["user"] = strings["config"]["step"]["user"]
en["options"]["step"]["init"]["data"] = data
en["services"] = services_json

with en_fname.open("w") as f:
    json.dump(en, f, indent=2, ensure_ascii=False)
    f.write("\n")