# dmm-python

A strictly-typed Python SDK for the [DMM Affiliate API v3](https://affiliate.dmm.com/api/).

Built on [`msgspec`](https://jcristharif.com/msgspec/) for fast JSON decoding and strict schema validation. HTTP execution is left entirely to the caller — the SDK only builds request data and decodes responses.

## Features

- Full type coverage for all 7 API endpoints
- Transport-agnostic: works with `urllib`, `requests`, or `httpx`
- Strict types via `msgspec` — no silent `None` coercions
- Affiliate ID validated at construction time

## Installation

```bash
pip install dmm-python

# With requests support
pip install dmm-python[requests]

# With httpx support
pip install dmm-python[httpx]
```

## Quick Start

```python
import requests
import msgspec
from dmm import (
    DMMClient,
    DMMSiteCode,
    DMMItemListRequestParams,
    DMMItemListResponseBody,
)

client = DMMClient(api_id="YOUR_API_ID", affiliate_id="YOUR_AFFILIATE_ID")
session = requests.Session()

params = DMMItemListRequestParams(site=DMMSiteCode.FANZA)
req = client.create_item_list_request_data(params)

response = session.send(req.to_requests_prepared_request())
response.raise_for_status()

body = msgspec.json.decode(response.content, type=DMMItemListResponseBody)

print(f"Total: {body.result.total_count}")
for item in body.result.items:
    print(item.title, item.price_info.price_start_at)
```

## Transport Options

```python
# stdlib — no extra dependencies
urllib_req = req.to_urllib_request()

# requests
prepared = req.to_requests_prepared_request()

# httpx
httpx_req = req.to_httpx_request()
```

## Docs

- [`docs/field-reference.md`](docs/field-reference.md) — Field-by-field comparison: official docs × Go SDK × this SDK
- [`docs/schema/`](docs/schema/) — JSON Schema for each endpoint's response body
