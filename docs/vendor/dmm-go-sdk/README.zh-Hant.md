# dmm-go-sdk — 結構體參考

從 [dmmlabo/dmm-go-sdk](https://github.com/dmmlabo/dmm-go-sdk)（commit `f67870f8`）擷取的 Go 結構體定義。

## 內容

| 檔案 | API 端點 |
|------|---------|
| `floor_list.md` | Floor List |
| `item_list.md` | Item List |
| `actress_search.md` | Actress Search |
| `genre_search.md` | Genre Search |
| `maker_search.md` | Maker Search |
| `series_search.md` | Series Search |
| `author_search.md` | Author Search |

每個檔案包含該端點的 `*Service`（request params）、`*RawResponse`、`*Response` 及所有巢狀結構體的完整 Go 原始碼，並附有指向 GitHub 對應行號的連結。

## 注意事項

- Go SDK 使用 [mapstructure](https://github.com/mitchellh/mapstructure) 而非 `encoding/json`，tag 鍵直接對應原始 JSON 欄位名稱。
- 結構體中沒有預設值的欄位在 mapstructure 下視為必填（key 缺失時不報錯，而是填入零值）。
- Go SDK 與實際 API 回應之間存在若干已知型別不符問題，詳見 `docs/api-coverage.md`。
