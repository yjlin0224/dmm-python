"""Generate JSON Schema for each API endpoint into docs/schema/<api>.json."""

import json
from pathlib import Path

import msgspec.json

from dmm import (
    DMMActressSearchResponseBody,
    DMMAuthorSearchResponseBody,
    DMMFloorListResponseBody,
    DMMGenreSearchResponseBody,
    DMMItemListResponseBody,
    DMMMakerSearchResponseBody,
    DMMSeriesSearchResponseBody,
)

APIS: list[tuple[str, type]] = [
    ("item_list", DMMItemListResponseBody),
    ("floor_list", DMMFloorListResponseBody),
    ("actress_search", DMMActressSearchResponseBody),
    ("genre_search", DMMGenreSearchResponseBody),
    ("maker_search", DMMMakerSearchResponseBody),
    ("series_search", DMMSeriesSearchResponseBody),
    ("author_search", DMMAuthorSearchResponseBody),
]

OUT_DIR = Path("docs/schema")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for name, response_type in APIS:
    schema = msgspec.json.schema(response_type)
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": name,
        **schema,
    }
    out = OUT_DIR.joinpath(f"{name}.schema.json")
    out.write_bytes(json.dumps(schema, ensure_ascii=False, indent=2).encode("utf-8"))
    print(f"  {out}")

print("Done.")
