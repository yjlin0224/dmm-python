# dmm-go-sdk — Struct Reference

Go struct definitions extracted from [dmmlabo/dmm-go-sdk](https://github.com/dmmlabo/dmm-go-sdk) (commit `f67870f8`).

## Contents

| File | API Endpoint |
|------|-------------|
| `floor_list.md` | Floor List |
| `item_list.md` | Item List |
| `actress_search.md` | Actress Search |
| `genre_search.md` | Genre Search |
| `maker_search.md` | Maker Search |
| `series_search.md` | Series Search |
| `author_search.md` | Author Search |

Each file contains the full Go source for that endpoint's `*Service` (request params), `*RawResponse`, `*Response`, and all nested structs, with a link to the exact line range on GitHub.

## Notes

- The Go SDK uses [mapstructure](https://github.com/mitchellh/mapstructure) rather than `encoding/json`, so tag keys map directly to raw JSON field names.
- Fields with no default in a struct are treated as required by mapstructure (missing keys produce zero values, not errors).
- Several known type mismatches exist between the Go SDK and actual API responses — see `docs/api-coverage.md` for details.
