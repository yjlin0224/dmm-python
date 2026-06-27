# DMM Affiliate API v3 — 三方規格對照

| 規格 | 來源 | 說明 |
|------|------|------|
| **官方文件** | [affiliate.dmm.com/api/](https://affiliate.dmm.com/api/)（離線鏡像：`docs/vendor/affiliate.dmm.com/`） | DMM 官方 API 文件 |
| **官方 Go SDK** | [dmmlabo/dmm-go-sdk](https://github.com/dmmlabo/dmm-go-sdk)（結構體：`docs/vendor/dmm-go-sdk/`） | DMM 官方提供的 Go 參考實作 |
| **本專案 Python SDK** | `src/dmm/` | 本專案實作，基於實測 JSON 驗證 |

## 凡例

| 標記 | 說明 |
|------|------|
| `必` | Request param：官方文件 `必須` 欄標有 ○ |
| `選` | Request param：官方文件 `必須` 欄為空 |

Response 欄位官方文件不標必/選，只記錄型別（從表格範例值推斷）。括號備註僅記載官方文件表格樣本與同頁範例 JSON 之間的差異。

官方 Go SDK 使用 `mapstructure` 解析（而非 `encoding/json`），struct 中無 default 的欄位等同必填，缺少零值處理。

本專案 Python SDK 欄位如有 property 換名，格式為 `_raw: type → property name: return_type`。

---

## 共通注意

- `api_id`、`affiliate_id`、`output`、`callback` 所有 request 都有，由 `DMMClient` 統一注入，不含於各 `RequestParams` struct。
- 官方 Go SDK 的 `*Service` struct 含 `ApiID`、`AffiliateID` 欄位，本專案 Python SDK 刻意排除。
- `result_count`、`first_position` 在官方文件表格與範例 JSON 均為 integer，一致。
- `status`、`total_count` 在 ItemList 的官方範例 JSON 亦為 integer（與 Article / Actress 端點不同）。

---

## 1. FloorList

### Request Params

| 欄位 | 官方文件 | 官方 Go SDK (`FloorService`) | 本專案 Python SDK (`DMMFloorListRequestParams`) |
|------|----------|------------------------------|------------------------------------------------|
| `api_id` | 必 string | `string` | （注入） |
| `affiliate_id` | 必 string | `string` | （注入） |
| （無業務欄位） | | | 空 struct |

### Response

| JSON 欄位 | 官方文件 | 官方 Go SDK | 本專案 Python SDK |
|-----------|----------|-------------|------------------|
| `result.site[].name` | string | `string` | `str` |
| `result.site[].code` | string | `string` | `DMMSiteCode` |
| `result.site[].service[].name` | string | `string` | `str` |
| `result.site[].service[].code` | string | `string` | `str` |
| `result.site[].service[].floor[].id` | integer（範例 JSON 為字串） | `int64` | `str` |
| `result.site[].service[].floor[].name` | string | `string` | `str` |
| `result.site[].service[].floor[].code` | string | `string` | `str` |

> FloorList 無分頁欄位，未繼承 `DMMResponseBodyResultPaginationMixin`。

---

## 2. ItemList

### Request Params

| 欄位 | 官方文件 | 官方 Go SDK (`ProductService`) | 本專案 Python SDK (`DMMItemListRequestParams`) |
|------|----------|--------------------------------|------------------------------------------------|
| `site` | 必 string | `string` | `DMMSiteCode` |
| `service` | 選 string | `string` | `Optional[str]` |
| `floor` | 選 string | `string` | `Optional[str]` |
| `hits` | 選 integer，預設 20，上限 100 | `int64` | `Annotated[int, Meta(ge=1, le=100)]`，預設 20 |
| `offset` | 選 integer，預設 1，上限 50000 | `int64` | `Annotated[int, Meta(ge=1, le=50000)]`，預設 1 |
| `sort` | 選 string | `string` | `DMMItemListSort` enum，預設 `rank` |
| `keyword` | 選 string | `string` | `Optional[str]` |
| `cid` | 選 string | `string` (`ContentID`) | `Optional[str]` |
| `article[]` + `article_id[]` | 選，兩個平行陣列 | `string` (`Article`, `ArticleID`) | 合併為 `list[DMMItemListRequestParamsArticle]`，序列化時展開 |
| `gte_date` / `lte_date` | 選，ISO8601 無時區 | `string` | `Annotated[Optional[datetime], Meta(tz=False)]` |
| `mono_stock` | 選 string | `string` (`Stock`) | `DMMItemListMonoStock` enum（含未文件化 `dmp`） |

### Response — 分頁

| JSON 欄位 | 官方文件 | 官方 Go SDK (`ProductResponse`) | 本專案 Python SDK (`DMMItemListResponseBodyResult`) |
|-----------|----------|---------------------------------|-----------------------------------------------------|
| `result.status` | integer | | `_status: int \| str` → property `status: int` |
| `result.result_count` | integer | `int64` | `int` |
| `result.total_count` | integer | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `result.first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `result.items` | array | `[]Item` | `list[...]`（無結果時為 `[]`，key 不缺失） |

### Response — Item 頂層

| JSON 欄位 | 官方文件 | 官方 Go SDK (`Item`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItem`) |
|-----------|----------|----------------------|--------------------------------------------------------|
| `service_code` | string | `string` | `str` |
| `service_name` | string | `string` | `str` |
| `floor_code` | string | `string` | `str` |
| `floor_name` | string | `string` | `str` |
| `category_name` | string | `string` | `str` |
| `content_id` | string | `string` | `str` |
| `product_id` | string | `string` | `str` |
| `title` | string | `string` | `str` |
| `date` | string | `string` | `_date: str` → property `date: datetime` |
| `volume` | integer（範例 JSON 為字串） | `string` \| absent | `_volume: str \| UNSET` → property `volume: int \| None`（支援 `"120"` 及 `"1:07:00"`） |
| `number` | integer | | `_number: str \| UnsetType` → property `number: Optional[int]`（型別待驗證） |
| `URL` | string | `string` | `url: str`（JSON name `URL`） |
| `affiliateURL` | string | `string` | `affiliate_url: str`（JSON name `affiliateURL`） |
| `review` | object | `ReviewInformation`（mapstructure 零值） | `DMMItemListResponseBodyResultItemReview \| UnsetType` |
| `imageURL` | object | `ImageURLList` | `image_url: DMMItemListResponseBodyResultItemImageURL`（JSON name `imageURL`） |
| `sampleImageURL` | object | `SampleImageURLList`（mapstructure 零值） | `sample_image_url: DMMItemListResponseBodyResultItemSampleImageURL \| UnsetType`（JSON name `sampleImageURL`） |
| `sampleMovieURL` | object | `SampleMovieURLList`（mapstructure 零值） | `sample_movie_url: DMMItemListResponseBodyResultItemSampleMovieURL \| UnsetType`（JSON name `sampleMovieURL`） |
| `tachiyomi` | object | | `DMMItemListResponseBodyResultItemTachiyomi \| UnsetType` |
| `prices` | object | `PriceInformation` | `price_info: DMMItemListResponseBodyResultItemPriceInfo`（JSON name `prices`） |
| `iteminfo` | object | `ItemInformation` | `item_info: DMMItemListResponseBodyResultItemItemInfo`（JSON name `iteminfo`） |
| `cdinfo` | object | `CdInformation`（mapstructure 零值） | `cd_info: DMMItemListResponseBodyResultItemCDInfo \| UnsetType`（JSON name `cdinfo`） |
| `jancode` | integer | `string`（mapstructure 零值） | `jan_code: str \| UnsetType`（JSON name `jancode`） |
| `isbn` | string | `string`（mapstructure 零值） | `str \| UnsetType` |
| `maker_product` | string | `string` (`ProductCode`） | `maker_product_code: str \| UnsetType`（JSON name `maker_product`） |
| `stock` | string | `string`（mapstructure 零值） | `str \| UnsetType` |
| `directory[]` | object array | | `_directories: list[...ItemInfoData] \| UnsetType` → property `directories: list[...]`（JSON name `directory`） |
| `campaign[]` | object array | | `_campaigns: list[...Campaign] \| UnsetType` → property `campaigns: list[...]`（JSON name `campaign`） |
| `URLsp` | 未文件化 | `string` (`URLMobile`） | `url_sp: str \| UnsetType`（JSON name `URLsp`） |
| `affiliateURLsp` | 未文件化 | `string` (`AffiliateURLMobile`） | `affiliate_url_sp: str \| UnsetType`（JSON name `affiliateURLsp`） |
| `comment` | 未文件化 | `string`（mapstructure 零值） | `str \| UnsetType` |
| `bandiInfo` | 未文件化 | `BandaiInformation` (`bandaiinfo`） | `bandai_info: DMMItemListResponseBodyResultItemBandaiInfo \| UnsetType`（JSON name `bandaiinfo`） |

### Response — review

| JSON 欄位 | 官方文件 | 官方 Go SDK (`ReviewInformation`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItemReview`) |
|-----------|----------|-----------------------------------|--------------------------------------------------------------|
| `count` | integer | `int64` | `int` |
| `average` | float（範例 JSON 為字串） | `float64`（mapstructure 自動轉型） | `_average: str` → property `average: float` |

### Response — imageURL

| JSON 欄位 | 官方文件 | 官方 Go SDK (`ImageURLList`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItemImageURL`) |
|-----------|----------|------------------------------|----------------------------------------------------------------|
| `list` | string | `string` | `str` |
| `small` | string | `string` | `str \| UnsetType` |
| `large` | string | `string` | `str \| UnsetType` |

> **備註：** `large` 僅存在於 digital 服務的作品。mono 作品的 `imageURL` 只有 `list` 和 `small`。大圖很可能是 API 回應中省略，而非 CDN 上不存在——網站本身也使用相同的 URL 規則。可嘗試將 `small` 網址結尾的 `ps` 替換為 `pl`（例如 `…ps.jpg` → `…pl.jpg`）來取得大封面。

### Response — sampleImageURL

| JSON 欄位 | 官方文件 | 官方 Go SDK (`SampleImageURLList`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItemSampleImageURL`) |
|-----------|----------|------------------------------------|-----------------------------------------------------------------------|
| `sample_s.image[]` | string array | `[]string`（`SmallSampleList.Image`） | property `sample_s_images` → `list[str]` |
| `sample_l.image[]` | string array | | property `sample_l_images` → `list[str]` |

### Response — sampleMovieURL

| JSON 欄位 | 官方文件 | 官方 Go SDK (`SampleMovieURLList`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItemSampleMovieURL`) |
|-----------|----------|------------------------------------|-----------------------------------------------------------------------|
| `size_476_306` | string | `string` | `str` |
| `size_560_360` | string | `string` | `str` |
| `size_644_414` | string | `string` | `str` |
| `size_720_480` | string | `string` | `str` |
| `pc_flag` | integer | `bool`（mapstructure 自動轉型） | `_pc_flag: int` → property `pc_flag: bool` |
| `sp_flag` | integer | `bool`（mapstructure 自動轉型） | `_sp_flag: int` → property `sp_flag: bool` |

### Response — prices

| JSON 欄位 | 官方文件 | 官方 Go SDK (`PriceInformation`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItemPriceInfo`) |
|-----------|----------|----------------------------------|------------------------------------------------------------------|
| `price` | string | `string` | `_price: str` → property `price_start_at: int` |
| `list_price` | string | `string` (`RetailPrice`） | `_list_price: str \| UnsetType` → property `list_price_start_at: Optional[int]` |
| `price_all` | 未文件化 | `string` | `_price_all: str \| UnsetType` → property `price_all_start_at: Optional[int]`（格式待驗證） |
| `deliveries` | object | `DistributionList` (`Distributions`） | `_deliveries: _DMMItemListResponseBodyResultItemPriceInfoDeliveries \| UnsetType` → property `deliveries: list[...]` |

### Response — prices.deliveries.delivery[]

| JSON 欄位 | 官方文件 | 官方 Go SDK (`Distribution`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItemPriceInfoDelivery`) |
|-----------|----------|-------------------------------|--------------------------------------------------------------------------|
| `type` | string | `string` | `str` |
| `price` | integer（範例 JSON 為字串） | `string` | `_price: str` → property `price: int` |
| `list_price` | 未文件化 | | `_list_price: str` → property `list_price: int` |

### Response — tachiyomi

| JSON 欄位 | 官方文件 | 官方 Go SDK | 本專案 Python SDK (`DMMItemListResponseBodyResultItemTachiyomi`) |
|-----------|----------|-------------|------------------------------------------------------------------|
| `URL` | string | | `url: str`（JSON name `URL`）（型別待驗證） |
| `affiliateURL` | string（文件拼錯為 `affilaiteURL`） | | `affiliate_url: str`（JSON name `affiliateURL`）（型別待驗證） |

### Response — iteminfo

| JSON 欄位 | 官方文件 | 官方 Go SDK (`ItemInformation`) | 本專案 Python SDK (`DMMItemListResponseBodyResultItemItemInfo`) |
|-----------|----------|---------------------------------|----------------------------------------------------------------|
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
| `keyword[]` | 未文件化 | `[]ItemComponent` | `_keyword: list[...ItemInfoData] \| UnsetType` → property `keywords: list[...]` |
| `artist[]` | 未文件化 | `[]ItemComponent` | `_artist: list[...ItemInfoDataWithRuby] \| UnsetType` → property `artists: list[...]` |
| `fighter[]` | 未文件化 | `[]ItemComponent` | `_fighter: list[...ItemInfoDataWithRuby] \| UnsetType` → property `fighters: list[...]` |

### Response — iteminfo[]（ItemComponent）

| JSON 欄位 | 官方文件 | 官方 Go SDK (`ItemComponent`) | 本專案 Python SDK |
|-----------|----------|-------------------------------|-------------------|
| `id` | integer | `string` | `_id: int \| str` → property `id: str`（返回型別考慮改為 `str \| None`） |
| `name` | string | `string` | `str` |
| `ruby` | string | | `str \| UnsetType`（僅 `ItemInfoDataWithRuby`，key 可能缺失） |

---

## 3. ActressSearch

### Request Params

| 欄位 | 官方文件 | 官方 Go SDK (`ActressService`) | 本專案 Python SDK (`DMMActressSearchRequestParams`) |
|------|----------|--------------------------------|------------------------------------------------------|
| `initial` | 選 string | `string` | `Optional[str]` |
| `actress_id` | 選 integer | `string` (`ActressID`) | `Optional[str]` |
| `keyword` | 選 string | `string` | `Optional[str]` |
| `gte_bust` / `lte_bust` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_waist` / `lte_waist` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_hip` / `lte_hip` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_height` / `lte_height` | 選 integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_birthday` / `lte_birthday` | 選 string（文件說 `yyyymmdd`，範例為 `1990-01-01`） | `string` | `Optional[date]`（ISO 格式） |
| `hits` | 選 integer，預設 20，上限 100 | `int64` | `Annotated[int, Meta(ge=1, le=100)]`，預設 20 |
| `offset` | 選 integer，預設 1 | `int64` | `Annotated[int, Meta(ge=1)]`，預設 1 |
| `sort` | 選 string，預設 `-name` | `string` | `Optional[DMMActressSearchSort]`（預設 `None`，不傳送） |

> 官方 Go SDK `ActressService`（request）亦含 `Bust`、`GteBust`...`LteBirthday` 等欄位，與 `Actress` response struct 重複。

### Response — 分頁

| JSON 欄位 | 官方文件 | 官方 Go SDK (`ActressResponse`) | 本專案 Python SDK (`DMMActressSearchResponseBodyResult`) |
|-----------|----------|---------------------------------|----------------------------------------------------------|
| `status` | integer（範例 JSON 為字串） | | `_status: int \| str` → property `status: int` |
| `result_count` | integer | `int64` | `int` |
| `total_count` | integer（範例 JSON 為字串） | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `actress[]`（整體） | array | `[]Actress`（mapstructure 零值） | `_actress: list[...] \| UnsetType` → property `actresses: list[...]`（無結果時 key absent） |

### Response — Actress

| JSON 欄位 | 官方文件 | 官方 Go SDK (`Actress`) | 本專案 Python SDK (`DMMActressSearchResponseBodyResultActress`) |
|-----------|----------|-------------------------|----------------------------------------------------------------|
| `id` | integer（範例 JSON 為字串） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `bust` | integer（範例 JSON 為字串） | `string`（含 `GteBust` / `LteBust`，混入 request 參數） | `_bust: Optional[str]` → property `bust: Optional[int]` |
| `waist` | integer（範例 JSON 為字串） | `string`（含 `GteWaist` / `LteWaist`，混入 request 參數） | `_waist: Optional[str]` → property `waist: Optional[int]` |
| `hip` | integer（範例 JSON 為字串） | `string`（含 `GteHip` / `LteHip`，混入 request 參數） | `_hip: Optional[str]` → property `hip: Optional[int]` |
| `height` | integer（範例 JSON 為字串或 null） | `string`（含 `GteHeight` / `LteHeight`，混入 request 參數） | `_height: Optional[str]` → property `height: Optional[int]` |
| `cup` | string | `string`（含 `GteCup` 等，混入 request） | `str \| UnsetType` |
| `birthday` | string（範例 JSON 有 null） | `string` (`Birthday`，含 `GteBirthday` / `LteBirthday`) | `Optional[date]` |
| `blood_type` | string（範例 JSON 有 null） | `string` | `Optional[str]` |
| `hobby` | string（範例 JSON 有 null） | `string` | `Optional[str]` |
| `prefectures` | string（範例 JSON 有 null） | `string` | `Optional[str]` |
| `imageURL`（整體） | object | `ActressImageList` | `image_url: DMMActressImageURL \| UnsetType`（JSON name `imageURL`） |
| `imageURL.small` | string | `string` | `str` |
| `imageURL.large` | string | `string` | `str` |
| `listURL`（整體） | object | `ActressProductList` | `list_url: DMMActressListURL`（JSON name `listURL`） |
| `listURL.digital` | string | `string` | `str` |
| `listURL.monthly` | string | `string` | `str` |
| `listURL.mono` | string | `string` | `str` |
| `listURL.ppm` | 未文件化 | `string` (`Ppm`) | `ppm: str \| UnsetType`（存在與否待驗證） |
| `listURL.rental` | 未文件化 | `string` (`Rental`) | `rental: str \| UnsetType`（存在與否待驗證） |

---

## 4. GenreSearch / MakerSearch / SeriesSearch / AuthorSearch

### Request Params（共通）

| 欄位 | 官方文件 | 官方 Go SDK (`*Service`) | 本專案 Python SDK (`*RequestParams`) |
|------|----------|--------------------------|--------------------------------------|
| `floor_id` | 必 string | `string` | `str` |
| `initial` | 選 string（AuthorSearch 為前綴比對，非頭文字） | `string` | `Optional[str]` |
| `hits` | 選 integer，預設 100，上限 500 | `int64` | `Annotated[int, Meta(ge=1, le=500)]`，預設 100 |
| `offset` | 選 integer，預設 1 | `int64` | `Annotated[int, Meta(ge=1)]`，預設 1 |

### Response — 共通分頁 + 樓層

| JSON 欄位 | 官方文件 | 官方 Go SDK (`*Response`) | 本專案 Python SDK (`DMMArticleSearchResponseBodyResultMixin`) |
|-----------|----------|---------------------------|--------------------------------------------------------------|
| `status` | integer（範例 JSON 為字串） | | `_status: int \| str` → property `status: int` |
| `result_count` | integer | `int64` | `int` |
| `total_count` | integer（範例 JSON 為字串） | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `site_name` | string | `string` | `str` |
| `site_code` | string | `string` | `DMMSiteCode` |
| `service_name` | string | `string` | `str` |
| `service_code` | string | `string` | `str` |
| `floor_id` | integer（範例 JSON 為字串） | `string` | `str` |
| `floor_name` | string | `string` | `str` |
| `floor_code` | string | `string` | `str` |

### GenreSearch — genre[]

| JSON 欄位 | 官方文件 | 官方 Go SDK (`Genre`) | 本專案 Python SDK (`DMMGenreSearchResponseBodyResultGenre`) |
|-----------|----------|-----------------------|-------------------------------------------------------------|
| `genre[]`（整體） | array | `[]Genre`（mapstructure 零值） | `_genre: list[...] \| UnsetType` → property `genres: list[...]`（無結果時 key absent） |
| `genre_id` | integer（範例 JSON 為字串） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `list_url` | string | `string` | `str \| UnsetType`（部分 floor 無此 key） |

### MakerSearch — maker[]

| JSON 欄位 | 官方文件 | 官方 Go SDK (`Maker`) | 本專案 Python SDK (`DMMMakerSearchResponseBodyResultMaker`) |
|-----------|----------|-----------------------|-------------------------------------------------------------|
| `maker[]`（整體） | array | `[]Maker`（mapstructure 零值） | `_maker: list[...] \| UnsetType` → property `makers: list[...]`（無結果時 key absent） |
| `maker_id` | integer（範例 JSON 為字串） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `another_name` | 未文件化 | | `str \| UnsetType` |
| `list_url` | string | `string` | `str \| UnsetType`（部分 floor 無此 key） |

### SeriesSearch — series[]

| JSON 欄位 | 官方文件 | 官方 Go SDK (`Series`) | 本專案 Python SDK (`DMMSeriesSearchResponseBodyResultSeries`) |
|-----------|----------|------------------------|--------------------------------------------------------------|
| `series[]`（整體） | array | `[]Series`（mapstructure 零值） | `_series: list[...] \| UnsetType` → property `series: list[...]`（無結果時 key absent） |
| `series_id` | integer（範例 JSON 為字串） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `list_url` | string | `string` | `str \| UnsetType`（部分 floor 無此 key） |

### AuthorSearch — author[]

| JSON 欄位 | 官方文件 | 官方 Go SDK (`Author`) | 本專案 Python SDK (`DMMAuthorSearchResponseBodyResultAuthor`) |
|-----------|----------|------------------------|--------------------------------------------------------------|
| `author[]`（整體） | array | `[]Author`（mapstructure 零值） | `_author: list[...] \| UnsetType` → property `authors: list[...]`（無結果時 key absent） |
| `author_id` | integer（範例 JSON 為字串） | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `another_name` | string | | `str \| UnsetType` |
| `list_url` | string | `string` | `str \| UnsetType`（部分 floor 無此 key） |

---

## 官方 Go SDK 已知問題

| 問題 | 欄位 |
|------|------|
| `DMMFloor.ID` 宣告 `int64`，JSON 實際為字串 | `floor.id` |
| `ReviewInformation.Average` 宣告 `float64`，JSON 實際為字串 `"5.00"` | `review.average` |
| `SampleMovieURL.PCFlag` / `SPFlag` 宣告 `bool`，JSON 實際為 int `0`/`1` | `sampleMovieURL.pc_flag` / `sp_flag` |
| `Actress` response struct 混入 `GteBust`、`LteBust` 等 request 參數欄位 | `actress.*` |
| `SampleImageURLList` 未定義 `sample_l` | `sampleImageURL.sample_l` |
| `Distribution` 未定義 `list_price` | `prices.deliveries.delivery[].list_price` |
| `ItemComponent` 未定義 `ruby` | `iteminfo.actress[].ruby` 等 |
| `PriceInformation.PriceAll` 定義但實測未見於 JSON | `prices.price_all` |
| `ActressProductList` 含 `Ppm`、`Rental`，本專案已定義但存在與否待驗證 | `listURL.ppm` / `listURL.rental` |
