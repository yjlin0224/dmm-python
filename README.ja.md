# dmm-python

[DMM アフィリエイト API v3](https://affiliate.dmm.com/api/) の厳密型 Python SDK。

[`msgspec`](https://jcristharif.com/msgspec/) による高速な JSON デコードと厳密なスキーマ検証を提供。HTTP の実行は呼び出し側に委ねる設計で、SDK はリクエストデータの構築とレスポンスのデコードのみを担う。

## 特徴

- 全 7 エンドポイントを完全カバー
- トランスポート非依存：`urllib`・`requests`・`httpx` に対応
- `msgspec` による厳密な型保証 — 暗黙の `None` 変換なし
- アフィリエイト ID をコンストラクタ時点で検証

## インストール

```bash
pip install dmm-python

# requests サポート付き
pip install dmm-python[requests]

# httpx サポート付き
pip install dmm-python[httpx]
```

## クイックスタート

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

print(f"総件数：{body.result.total_count}")
for item in body.result.items:
    print(item.title, item.price_info.price_start_at)
```

## トランスポートオプション

```python
# 標準ライブラリ — 追加依存なし
urllib_req = req.to_urllib_request()

# requests
prepared = req.to_requests_prepared_request()

# httpx
httpx_req = req.to_httpx_request()
```

## ドキュメント

- [`docs/field-reference.md`](docs/field-reference.md) — フィールド対照表：公式ドキュメント × Go SDK × 本 SDK
- [`docs/schema/`](docs/schema/) — 各エンドポイントのレスポンスボディ JSON Schema
