# dmm-python

[DMM 聯盟 API v3](https://affiliate.dmm.com/api/) 的嚴格型別 Python SDK。

基於 [`msgspec`](https://jcristharif.com/msgspec/) 實現快速 JSON 解碼與嚴格型別驗證。HTTP 執行完全交由呼叫端處理——SDK 只負責建構請求資料與解碼回應。

## 特色

- 完整覆蓋全部 7 個 API 端點
- 傳輸層無關：支援 `urllib`、`requests`、`httpx`
- 透過 `msgspec` 強制型別——不會靜默轉成 `None`
- Affiliate ID 在建構時即驗證

## 安裝

```bash
pip install dmm-python

# 附帶 requests 支援
pip install dmm-python[requests]

# 附帶 httpx 支援
pip install dmm-python[httpx]
```

## 快速開始

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

print(f"總筆數：{body.result.total_count}")
for item in body.result.items:
    print(item.title, item.price_info.price_start_at)
```

## 傳輸層選項

```python
# 標準函式庫——無額外相依
urllib_req = req.to_urllib_request()

# requests
prepared = req.to_requests_prepared_request()

# httpx
httpx_req = req.to_httpx_request()
```

## 文件

- [`docs/field-reference.md`](docs/field-reference.md) — 逐欄位對照：官方文件 × Go SDK × 本 SDK
- [`docs/schema/`](docs/schema/) — 各端點 Response body 的 JSON Schema
