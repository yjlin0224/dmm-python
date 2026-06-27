# DMM アフィリエイト API v3 — 三者仕様対照表

| 仕様 | ソース | 説明 |
|------|--------|------|
| **公式ドキュメント** | [affiliate.dmm.com/api/](https://affiliate.dmm.com/api/)（オフラインミラー：`docs/vendor/affiliate.dmm.com/`） | DMM 公式 API ドキュメント |
| **公式 Go SDK** | [dmmlabo/dmm-go-sdk](https://github.com/dmmlabo/dmm-go-sdk)（構造体：`docs/vendor/dmm-go-sdk/`） | DMM 公式 Go リファレンス実装 |
| **本プロジェクト Python SDK** | `src/dmm/` | 本プロジェクトの実装、実測 JSON による検証済み |

## 凡例

| マーカー | 説明 |
|----------|------|
| `必` | リクエストパラメータ：公式ドキュメントの `必須` 列に ○ あり |
| `選` | リクエストパラメータ：`必須` 列が空 |

レスポンスフィールドに必須/任意のマーカーはなく、型のみを記録する（テーブルのサンプル値から推定）。括弧内の注記は、公式ドキュメント HTML テーブルのサンプルと同ページの JSON 例が食い違う場合にのみ追記する。

公式 Go SDK は `encoding/json` ではなく `mapstructure` でデコードするため、デフォルト値のないフィールドは実質必須扱いとなり、キーが欠けた場合はゼロ値が入る。

本プロジェクト Python SDK でプロパティにより名前が変わるフィールドは `_raw: type → property name: return_type` の形式で示す。

---

## 共通事項

- `api_id`、`affiliate_id`、`output`、`callback` はすべてのリクエストに存在し、`DMMClient` が一括注入する。個別の `RequestParams` 構造体には含まれない。
- 公式 Go SDK の `*Service` 構造体には `ApiID`・`AffiliateID` フィールドがあるが、本 Python SDK では意図的に除外している。
- `result_count`・`first_position` は公式ドキュメントのテーブルと JSON 例のいずれも integer で一致。
- `status`・`total_count` は ItemList の公式 JSON 例でも integer（Article / Actress エンドポイントとは異なる）。

---

## 1. FloorList

### リクエストパラメータ

| フィールド | 公式ドキュメント | 公式 Go SDK (`FloorService`) | 本プロジェクト Python SDK (`DMMFloorListRequestParams`) |
|------------|------------------|------------------------------|----------------------------------------------------------|
| `api_id` | 必 string | `string` | （注入） |
| `affiliate_id` | 必 string | `string` | （注入） |
| （業務フィールドなし） | | | 空構造体 |

### レスポンス

| JSON フィールド | 公式ドキュメント | 公式 Go SDK | 本プロジェクト Python SDK |
|----------------|------------------|-------------|--------------------------|
| `result.site[].name` | string | `string` | `str` |
| `result.site[].code` | string | `string` | `DMMSiteCode` |
| `result.site[].service[].name` | string | `string` | `str` |
| `result.site[].service[].code` | string | `string` | `str` |
| `result.site[].service[].floor[].id` | integer（JSON 例は文字列） | `int64` | `str` |
| `result.site[].service[].floor[].name` | string | `string` | `str` |
| `result.site[].service[].floor[].code` | string | `string` | `str` |

> FloorList はページネーションフィールドを持たず、`DMMResponseBodyResultPaginationMixin` を継承しない。

---

## 2. ItemList

### リクエストパラメータ

| フィールド | 公式ドキュメント | 公式 Go SDK (`ProductService`) | 本プロジェクト Python SDK (`DMMItemListRequestParams`) |
|------------|------------------|---------------------------------|--------------------------------------------------------|
| `site` | 必 string | `string` | `DMMSiteCode` |
| `service` | 選 string | `string` | `Optional[str]` |
| `floor` | 選 string | `string` | `Optional[str]` |
| `hits` | 選 integer、デフォルト 20、上限 100 | `int64` | `Annotated[int, Meta(ge=1, le=100)]`、デフォルト 20 |
| `offset` | 選 integer、デフォルト 1、上限 50000 | `int64` | `Annotated[int, Meta(ge=1, le=50000)]`、デフォルト 1 |
| `sort` | 選 string | `string` | `DMMItemListSort` 列挙型、デフォルト `rank` |
| `keyword` | 選 string | `string` | `Optional[str]` |
| `cid` | 選 string | `string` (`ContentID`) | `Optional[str]` |
| `article[]` + `article_id[]` | 選、2 つの並列配列 | `string` (`Article`, `ArticleID`) | `list[DMMItemListRequestParamsArticle]` に統合、シリアライズ時に展開 |
| `gte_date` / `lte_date` | 選、ISO8601 タイムゾーンなし | `string` | `Annotated[Optional[datetime], Meta(tz=False)]` |
| `mono_stock` | 選 string | `string` (`Stock`) | `DMMItemListMonoStock` 列挙型（未文書化の `dmp` を含む） |

### レスポンス — ページネーション

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`ProductResponse`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResult`) |
|----------------|------------------|---------------------------------|-------------------------------------------------------------|
| `result.status` | integer | | `_status: int \| str` → property `status: int` |
| `result.result_count` | integer | `int64` | `int` |
| `result.total_count` | integer | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `result.first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `result.items` | array | `[]Item` | `list[...]`（結果なしの場合は `[]`、キーは欠けない） |

### レスポンス — Item（トップレベル）

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`Item`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItem`) |
|----------------|------------------|----------------------|------------------------------------------------------------------|
| `service_code` | string | `string` | `str` |
| `service_name` | string | `string` | `str` |
| `floor_code` | string | `string` | `str` |
| `floor_name` | string | `string` | `str` |
| `category_name` | string | `string` | `str` |
| `content_id` | string | `string` | `str` |
| `product_id` | string | `string` | `str` |
| `title` | string | `string` | `str` |
| `date` | string | `string` | `_date: str` → property `date: datetime` |
| `volume` | integer（JSON 例は文字列） | `string` \| absent | `_volume: str \| UNSET` → property `volume: int \| None`（`"120"` および `"1:07:00"` 形式に対応） |
| `number` | integer | | `_number: str \| UnsetType` → property `number: Optional[int]`（型は未検証） |
| `URL` | string | `string` | `url: str`（JSON name `URL`） |
| `affiliateURL` | string | `string` | `affiliate_url: str`（JSON name `affiliateURL`） |
| `review` | object | `ReviewInformation`（mapstructure ゼロ値） | `DMMItemListResponseBodyResultItemReview \| UnsetType` |
| `imageURL` | object | `ImageURLList` | `image_url: DMMItemListResponseBodyResultItemImageURL`（JSON name `imageURL`） |
| `sampleImageURL` | object | `SampleImageURLList`（mapstructure ゼロ値） | `sample_image_url: DMMItemListResponseBodyResultItemSampleImageURL \| UnsetType`（JSON name `sampleImageURL`） |
| `sampleMovieURL` | object | `SampleMovieURLList`（mapstructure ゼロ値） | `sample_movie_url: DMMItemListResponseBodyResultItemSampleMovieURL \| UnsetType`（JSON name `sampleMovieURL`） |
| `tachiyomi` | object | | `DMMItemListResponseBodyResultItemTachiyomi \| UnsetType` |
| `prices` | object | `PriceInformation` | `price_info: DMMItemListResponseBodyResultItemPriceInfo`（JSON name `prices`） |
| `iteminfo` | object | `ItemInformation` | `item_info: DMMItemListResponseBodyResultItemItemInfo`（JSON name `iteminfo`） |
| `cdinfo` | object | `CdInformation`（mapstructure ゼロ値） | `cd_info: DMMItemListResponseBodyResultItemCDInfo \| UnsetType`（JSON name `cdinfo`） |
| `jancode` | integer | `string`（mapstructure ゼロ値） | `jan_code: str \| UnsetType`（JSON name `jancode`） |
| `isbn` | string | `string`（mapstructure ゼロ値） | `str \| UnsetType` |
| `maker_product` | string | `string` (`ProductCode`) | `maker_product_code: str \| UnsetType`（JSON name `maker_product`） |
| `stock` | string | `string`（mapstructure ゼロ値） | `str \| UnsetType` |
| `directory[]` | object array | | `_directories: list[...ItemInfoData] \| UnsetType` → property `directories: list[...]`（JSON name `directory`） |
| `campaign[]` | object array | | `_campaigns: list[...Campaign] \| UnsetType` → property `campaigns: list[...]`（JSON name `campaign`） |
| `URLsp` | 未文書化 | `string` (`URLMobile`) | `url_sp: str \| UnsetType`（JSON name `URLsp`） |
| `affiliateURLsp` | 未文書化 | `string` (`AffiliateURLMobile`) | `affiliate_url_sp: str \| UnsetType`（JSON name `affiliateURLsp`） |
| `comment` | 未文書化 | `string`（mapstructure ゼロ値） | `str \| UnsetType` |
| `bandiInfo` | 未文書化 | `BandaiInformation` (`bandaiinfo`) | `bandai_info: DMMItemListResponseBodyResultItemBandaiInfo \| UnsetType`（JSON name `bandaiinfo`） |

### レスポンス — review

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`ReviewInformation`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemReview`) |
|----------------|------------------|-------------------------------------|-----------------------------------------------------------------------|
| `count` | integer | `int64` | `int` |
| `average` | float（JSON 例は文字列） | `float64`（mapstructure 自動変換） | `_average: str` → property `average: float` |

### レスポンス — imageURL

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`ImageURLList`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemImageURL`) |
|----------------|------------------|-------------------------------|--------------------------------------------------------------------------|
| `list` | string | `string` | `str` |
| `small` | string | `string` | `str \| UnsetType` |
| `large` | string | `string` | `str \| UnsetType` |

> **備考:** `large` は digital サービスの作品にのみ存在します。mono の作品には `list` と `small` のみが含まれます。大サイズの画像は CDN 上には存在するものの API レスポンスから省略されている可能性があり、ウェブサイト自体も同じ URL パターンを使用しています。取得するには `small` の URL 末尾の `ps` を `pl` に置換してください（例: `…ps.jpg` → `…pl.jpg`）。

### レスポンス — sampleImageURL

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`SampleImageURLList`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemSampleImageURL`) |
|----------------|------------------|-------------------------------------|--------------------------------------------------------------------------------|
| `sample_s.image[]` | string array | `[]string`（`SmallSampleList.Image`） | property `sample_s_images` → `list[str]` |
| `sample_l.image[]` | string array | | property `sample_l_images` → `list[str]` |

### レスポンス — sampleMovieURL

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`SampleMovieURLList`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemSampleMovieURL`) |
|----------------|------------------|-------------------------------------|--------------------------------------------------------------------------------|
| `size_476_306` | string | `string` | `str` |
| `size_560_360` | string | `string` | `str` |
| `size_644_414` | string | `string` | `str` |
| `size_720_480` | string | `string` | `str` |
| `pc_flag` | integer | `bool`（mapstructure 自動変換） | `_pc_flag: int` → property `pc_flag: bool` |
| `sp_flag` | integer | `bool`（mapstructure 自動変換） | `_sp_flag: int` → property `sp_flag: bool` |

### レスポンス — prices

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`PriceInformation`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemPriceInfo`) |
|----------------|------------------|-----------------------------------|---------------------------------------------------------------------------|
| `price` | string | `string` | `_price: str` → property `price_start_at: int` |
| `list_price` | string | `string` (`RetailPrice`) | `_list_price: str \| UnsetType` → property `list_price_start_at: Optional[int]` |
| `price_all` | 未文書化 | `string` | `_price_all: str \| UnsetType` → property `price_all_start_at: Optional[int]`（形式未検証） |
| `deliveries` | object | `DistributionList` (`Distributions`) | `_deliveries: _DMMItemListResponseBodyResultItemPriceInfoDeliveries \| UnsetType` → property `deliveries: list[...]` |

### レスポンス — prices.deliveries.delivery[]

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`Distribution`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemPriceInfoDelivery`) |
|----------------|------------------|---------------------------------|----------------------------------------------------------------------------------|
| `type` | string | `string` | `str` |
| `price` | integer（JSON 例は文字列） | `string` | `_price: str` → property `price: int` |
| `list_price` | 未文書化 | | `_list_price: str` → property `list_price: int` |

### レスポンス — tachiyomi

| JSON フィールド | 公式ドキュメント | 公式 Go SDK | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemTachiyomi`) |
|----------------|------------------|-------------|---------------------------------------------------------------------------|
| `URL` | string | | `url: str`（JSON name `URL`）（型未検証） |
| `affiliateURL` | string（ドキュメントは `affilaiteURL` と誤記） | | `affiliate_url: str`（JSON name `affiliateURL`）（型未検証） |

### レスポンス — iteminfo

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`ItemInformation`) | 本プロジェクト Python SDK (`DMMItemListResponseBodyResultItemItemInfo`) |
|----------------|------------------|---------------------------------|-------------------------------------------------------------------------|
| `genre[]` | object array | `[]ItemComponent` | `_genre: list[...ItemInfoData] \| UnsetType` → property `genres: list[...]` |
| `series[]` | object array | `[]ItemComponent` | `_series: list[...ItemInfoData] \| UnsetType` → property `series: list[...]` |
| `maker[]` | object array | `[]ItemComponent` | `_maker: list[...ItemInfoData] \| UnsetType` → property `makers: list[...]` |
| `label[]` | object array | `[]ItemComponent` | `_label: list[...ItemInfoData] \| UnsetType` → property `labels: list[...]` |
| `type[]` | object array | | `_type: list[...ItemInfoData] \| UnsetType` → property `types: list[...]` |
| `color[]` | object array | `[]ItemComponent` | `_color: list[...ItemInfoData] \| UnsetType` → property `colors: list[...]` |
| `size[]` | object array | `[]ItemComponent` | `_size: list[...ItemInfoData] \| UnsetType` → property `sizes: list[...]` |
| `actor[]` | object array | `[]ItemComponent` | `_actor: list[...ItemInfoDataWithRuby] \| UnsetType` → property `actors: list[...]` |
| `actress[]` | object array | `[]ItemComponent` | `_actress: list[...ItemInfoDataWithRuby] \| UnsetType` → property `actresses: list[...]` |
| `director[]` | object array | `[]ItemComponent` | `_director: list[...ItemInfoDataWithRuby] \| UnsetType` → property `directors: list[...]` |
| `author[]` | object array | `[]ItemComponent` | `_author: list[...ItemInfoDataWithRuby] \| UnsetType` → property `authors: list[...]` |
| `keyword[]` | 未文書化 | `[]ItemComponent` | `_keyword: list[...ItemInfoData] \| UnsetType` → property `keywords: list[...]` |
| `artist[]` | 未文書化 | `[]ItemComponent` | `_artist: list[...ItemInfoDataWithRuby] \| UnsetType` → property `artists: list[...]` |
| `fighter[]` | 未文書化 | `[]ItemComponent` | `_fighter: list[...ItemInfoDataWithRuby] \| UnsetType` → property `fighters: list[...]` |

### レスポンス — iteminfo[]（ItemComponent）

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`ItemComponent`) | 本プロジェクト Python SDK |
|----------------|------------------|-------------------------------|--------------------------|
| `id` | integer | `string` | `_id: int \| str` → property `id: str`（戻り値型を `str \| None` に変更することも検討） |
| `name` | string | `string` | `str` |
| `ruby` | string | | `str \| UnsetType`（`ItemInfoDataWithRuby` のみ、キーが欠けることあり） |

---

## 3. ActressSearch

### リクエストパラメータ

| フィールド | 公式ドキュメント | 公式 Go SDK (`ActressService`) | 本プロジェクト Python SDK (`DMMActressSearchRequestParams`) |
|------------|------------------|---------------------------------|--------------------------------------------------------------|
| `initial` | 選 string | `string` | `Optional[str]` |
| `actress_id` | 選 integer | `string` (`ActressID`) | `Optional[str]` |
| `keyword` | 選 string | `string` | `Optional[str]` |
| `gte_bust` / `lte_bust` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_waist` / `lte_waist` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_hip` / `lte_hip` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_height` / `lte_height` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_birthday` / `lte_birthday` | 選 string（ドキュメントは `yyyymmdd`、例は `1990-01-01`） | `string` | `Optional[date]`（ISO 形式） |
| `hits` | 選 integer、デフォルト 20、上限 100 | `int64` | `Annotated[int, Meta(ge=1, le=100)]`、デフォルト 20 |
| `offset` | 選 integer、デフォルト 1 | `int64` | `Annotated[int, Meta(ge=1)]`、デフォルト 1 |
| `sort` | 選 string、デフォルト `-name` | `string` | `Optional[DMMActressSearchSort]`（デフォルト `None`、送信しない） |

> 公式 Go SDK `ActressService`（リクエスト）には `Bust`・`GteBust`…`LteBirthday` 等のフィールドも含まれており、`Actress` レスポンス構造体と重複している。

### レスポンス — ページネーション

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`ActressResponse`) | 本プロジェクト Python SDK (`DMMActressSearchResponseBodyResult`) |
|----------------|------------------|---------------------------------|------------------------------------------------------------------|
| `status` | integer（JSON 例は文字列） | | `_status: int \| str` → property `status: int` |
| `result_count` | integer | `int64` | `int` |
| `total_count` | integer（JSON 例は文字列） | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `actress[]`（コンテナ） | array | `[]Actress`（mapstructure ゼロ値） | `_actress: list[...] \| UnsetType` → property `actresses: list[...]`（結果なしの場合キー欠け） |

### レスポンス — Actress

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`Actress`) | 本プロジェクト Python SDK (`DMMActressSearchResponseBodyResultActress`) |
|----------------|------------------|-------------------------|-------------------------------------------------------------------------|
| `id` | integer（JSON 例は文字列） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `bust` | integer（JSON 例は文字列） | `string`（`GteBust`/`LteBust` 混入） | `_bust: Optional[str]` → property `bust: Optional[int]` |
| `waist` | integer（JSON 例は文字列） | `string`（`GteWaist`/`LteWaist` 混入） | `_waist: Optional[str]` → property `waist: Optional[int]` |
| `hip` | integer（JSON 例は文字列） | `string`（`GteHip`/`LteHip` 混入） | `_hip: Optional[str]` → property `hip: Optional[int]` |
| `height` | integer（JSON 例は文字列または null） | `string`（`GteHeight`/`LteHeight` 混入） | `_height: Optional[str]` → property `height: Optional[int]` |
| `cup` | string | `string`（`GteCup` 等混入） | `str \| UnsetType` |
| `birthday` | string（JSON 例に null あり） | `string`（`Birthday`、`GteBirthday`/`LteBirthday` 混入） | `Optional[date]` |
| `blood_type` | string（JSON 例に null あり） | `string` | `Optional[str]` |
| `hobby` | string（JSON 例に null あり） | `string` | `Optional[str]` |
| `prefectures` | string（JSON 例に null あり） | `string` | `Optional[str]` |
| `imageURL`（コンテナ） | object | `ActressImageList` | `image_url: DMMActressImageURL \| UnsetType`（JSON name `imageURL`） |
| `imageURL.small` | string | `string` | `str` |
| `imageURL.large` | string | `string` | `str` |
| `listURL`（コンテナ） | object | `ActressProductList` | `list_url: DMMActressListURL`（JSON name `listURL`） |
| `listURL.digital` | string | `string` | `str` |
| `listURL.monthly` | string | `string` | `str` |
| `listURL.mono` | string | `string` | `str` |
| `listURL.ppm` | 未文書化 | `string` (`Ppm`) | `ppm: str \| UnsetType`（存在有無未検証） |
| `listURL.rental` | 未文書化 | `string` (`Rental`) | `rental: str \| UnsetType`（存在有無未検証） |

---

## 4. GenreSearch / MakerSearch / SeriesSearch / AuthorSearch

### リクエストパラメータ（共通）

| フィールド | 公式ドキュメント | 公式 Go SDK (`*Service`) | 本プロジェクト Python SDK (`*RequestParams`) |
|------------|------------------|--------------------------|----------------------------------------------|
| `floor_id` | 必 string | `string` | `str` |
| `initial` | 選 string（AuthorSearch は前方一致、頭文字ではない） | `string` | `Optional[str]` |
| `hits` | 選 integer、デフォルト 100、上限 500 | `int64` | `Annotated[int, Meta(ge=1, le=500)]`、デフォルト 100 |
| `offset` | 選 integer、デフォルト 1 | `int64` | `Annotated[int, Meta(ge=1)]`、デフォルト 1 |

### レスポンス — 共通ページネーション＋フロア

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`*Response`) | 本プロジェクト Python SDK (`DMMArticleSearchResponseBodyResultMixin`) |
|----------------|------------------|---------------------------|-----------------------------------------------------------------------|
| `status` | integer（JSON 例は文字列） | | `_status: int \| str` → property `status: int` |
| `result_count` | integer | `int64` | `int` |
| `total_count` | integer（JSON 例は文字列） | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `site_name` | string | `string` | `str` |
| `site_code` | string | `string` | `DMMSiteCode` |
| `service_name` | string | `string` | `str` |
| `service_code` | string | `string` | `str` |
| `floor_id` | integer（JSON 例は文字列） | `string` | `str` |
| `floor_name` | string | `string` | `str` |
| `floor_code` | string | `string` | `str` |

### GenreSearch — genre[]

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`Genre`) | 本プロジェクト Python SDK (`DMMGenreSearchResponseBodyResultGenre`) |
|----------------|------------------|-----------------------|----------------------------------------------------------------------|
| `genre[]`（コンテナ） | array | `[]Genre`（mapstructure ゼロ値） | `_genre: list[...] \| UnsetType` → property `genres: list[...]`（結果なしの場合キー欠け） |
| `genre_id` | integer（JSON 例は文字列） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `list_url` | string | `string` | `str \| UnsetType`（フロアによりキー欠けあり） |

### MakerSearch — maker[]

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`Maker`) | 本プロジェクト Python SDK (`DMMMakerSearchResponseBodyResultMaker`) |
|----------------|------------------|-----------------------|----------------------------------------------------------------------|
| `maker[]`（コンテナ） | array | `[]Maker`（mapstructure ゼロ値） | `_maker: list[...] \| UnsetType` → property `makers: list[...]`（結果なしの場合キー欠け） |
| `maker_id` | integer（JSON 例は文字列） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `another_name` | 未文書化 | | `str \| UnsetType` |
| `list_url` | string | `string` | `str \| UnsetType`（フロアによりキー欠けあり） |

### SeriesSearch — series[]

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`Series`) | 本プロジェクト Python SDK (`DMMSeriesSearchResponseBodyResultSeries`) |
|----------------|------------------|------------------------|-----------------------------------------------------------------------|
| `series[]`（コンテナ） | array | `[]Series`（mapstructure ゼロ値） | `_series: list[...] \| UnsetType` → property `series: list[...]`（結果なしの場合キー欠け） |
| `series_id` | integer（JSON 例は文字列） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `list_url` | string | `string` | `str \| UnsetType`（フロアによりキー欠けあり） |

### AuthorSearch — author[]

| JSON フィールド | 公式ドキュメント | 公式 Go SDK (`Author`) | 本プロジェクト Python SDK (`DMMAuthorSearchResponseBodyResultAuthor`) |
|----------------|------------------|------------------------|-----------------------------------------------------------------------|
| `author[]`（コンテナ） | array | `[]Author`（mapstructure ゼロ値） | `_author: list[...] \| UnsetType` → property `authors: list[...]`（結果なしの場合キー欠け） |
| `author_id` | integer（JSON 例は文字列） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `another_name` | string | | `str \| UnsetType` |
| `list_url` | string | `string` | `str \| UnsetType`（フロアによりキー欠けあり） |

---

## 公式 Go SDK の既知の問題

| 問題 | フィールド |
|------|-----------|
| `DMMFloor.ID` が `int64` 宣言だが JSON は文字列 | `floor.id` |
| `ReviewInformation.Average` が `float64` 宣言だが JSON は文字列 `"5.00"` | `review.average` |
| `SampleMovieURL.PCFlag` / `SPFlag` が `bool` 宣言だが JSON は int `0`/`1` | `sampleMovieURL.pc_flag` / `sp_flag` |
| `Actress` レスポンス構造体に `GteBust`・`LteBust` 等のリクエストパラメータが混入 | `actress.*` |
| `SampleImageURLList` が `sample_l` を未定義 | `sampleImageURL.sample_l` |
| `Distribution` が `list_price` を未定義 | `prices.deliveries.delivery[].list_price` |
| `ItemComponent` が `ruby` を未定義 | `iteminfo.actress[].ruby` 等 |
| `PriceInformation.PriceAll` は定義されているが実測 JSON では未確認 | `prices.price_all` |
| `ActressProductList` が `Ppm`・`Rental` を定義、本プロジェクトでも定義済みだが存在有無は未検証 | `listURL.ppm` / `listURL.rental` |
