"""Validate the published schema, example, and important field constraints."""

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


root = Path(__file__).resolve().parents[1]
schema = json.loads((root / "skills/work-unit/references/work-unit.schema.json").read_text())
example = json.loads((root / "docs/resources/work-unit.example.json").read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
validator.validate(example)

invalid_records = []
for count in [0, 3, 5]:
    invalid = copy.deepcopy(example)
    invalid["emojis"] = ["🦊"] * count
    invalid_records.append(invalid)
for field in schema["required"]:
    invalid = copy.deepcopy(example)
    del invalid[field]
    invalid_records.append(invalid)
for field, value in [("worktree_paths", ["relative/path"]), ("merge_request_urls", ["https://example.com"]), ("verified_at", "yesterday")]:
    invalid = copy.deepcopy(example)
    invalid["implementations"][0][field] = value
    invalid_records.append(invalid)

for invalid in invalid_records:
    if validator.is_valid(invalid):
        raise AssertionError(f"Invalid record accepted: {invalid}")

print(f"Schema and example valid; {len(invalid_records)} invalid records rejected.")
