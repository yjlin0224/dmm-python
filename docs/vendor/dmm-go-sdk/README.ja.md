# dmm-go-sdk — 構造体リファレンス

[dmmlabo/dmm-go-sdk](https://github.com/dmmlabo/dmm-go-sdk)（コミット `f67870f8`）から抽出した Go 構造体定義です。

## 内容

| ファイル | API エンドポイント |
|----------|------------------|
| `floor_list.md` | フロアリスト |
| `item_list.md` | 商品情報リスト |
| `actress_search.md` | 女優検索 |
| `genre_search.md` | ジャンル検索 |
| `maker_search.md` | メーカー検索 |
| `series_search.md` | シリーズ検索 |
| `author_search.md` | 作者検索 |

各ファイルには、そのエンドポイントの `*Service`（リクエストパラメータ）、`*RawResponse`、`*Response`、およびすべてのネスト構造体の Go ソースコードが含まれており、GitHub 上の該当行へのリンクも記載されています。

## 注意事項

- Go SDK は `encoding/json` ではなく [mapstructure](https://github.com/mitchellh/mapstructure) を使用しています。タグのキーは JSON フィールド名と直接対応しています。
- 構造体でデフォルト値のないフィールドは mapstructure によって必須扱いとなります（キーが欠落した場合はエラーにならずゼロ値になります）。
- Go SDK と実際の API レスポンスの間に型の不一致がいくつか存在します。詳細は `docs/api-coverage.md` を参照してください。
