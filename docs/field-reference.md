# DMM Affiliate API v3 — Three-Way Spec Comparison

| Spec | Source | Description |
|------|--------|-------------|
| **Official Docs** | [affiliate.dmm.com/api/](https://affiliate.dmm.com/api/) (offline mirror: `docs/vendor/affiliate.dmm.com/`) | DMM official API documentation |
| **Official Go SDK** | [dmmlabo/dmm-go-sdk](https://github.com/dmmlabo/dmm-go-sdk) (structs: `docs/vendor/dmm-go-sdk/`) | Official Go reference implementation by DMM |
| **This Python SDK** | `src/dmm/` | This project's implementation, validated against live JSON |

## Legend

| Marker | Description |
|--------|-------------|
| `req` | Request param: marked ○ in the official docs `必須` column |
| `opt` | Request param: `必須` column is empty |

Response fields carry no required/optional marker in the official docs — only the type is recorded (inferred from table sample values). Parenthetical notes are added only when the official docs HTML table sample and the same-page JSON example disagree.

The official Go SDK uses `mapstructure` for decoding (not `encoding/json`). Fields without a default value are effectively required; missing keys receive zero values rather than errors.

For Python SDK fields that are renamed via a property, the format is `_raw: type → property name: return_type`.

---

## Common Notes

- `api_id`, `affiliate_id`, `output`, `callback` are present on every request and injected by `DMMClient`; they are not included in individual `RequestParams` structs.
- The official Go SDK `*Service` structs include `ApiID` and `AffiliateID` fields; this Python SDK intentionally excludes them.
- `result_count` and `first_position` are integer in both the official docs table and the JSON example, with no discrepancy.
- `status` and `total_count` are also integer in the ItemList JSON example (unlike the Article / Actress endpoints).

---

## 1. FloorList

### Request Params

| Field | Official Docs | Official Go SDK (`FloorService`) | This Python SDK (`DMMFloorListRequestParams`) |
|-------|---------------|----------------------------------|------------------------------------------------|
| `api_id` | req string | `string` | (injected) |
| `affiliate_id` | req string | `string` | (injected) |
| (no business fields) | | | empty struct |

### Response

| JSON Field | Official Docs | Official Go SDK | This Python SDK |
|------------|---------------|-----------------|-----------------|
| `result.site[].name` | string | `string` | `str` |
| `result.site[].code` | string | `string` | `DMMSiteCode` |
| `result.site[].service[].name` | string | `string` | `str` |
| `result.site[].service[].code` | string | `string` | `str` |
| `result.site[].service[].floor[].id` | integer (JSON example is string) | `int64` | `str` |
| `result.site[].service[].floor[].name` | string | `string` | `str` |
| `result.site[].service[].floor[].code` | string | `string` | `str` |

> FloorList has no pagination fields and does not inherit `DMMResponseBodyResultPaginationMixin`.

---

## 2. ItemList

### Request Params

| Field | Official Docs | Official Go SDK (`ProductService`) | This Python SDK (`DMMItemListRequestParams`) |
|-------|---------------|------------------------------------|----------------------------------------------|
| `site` | req string | `string` | `DMMSiteCode` |
| `service` | opt string | `string` | `Optional[str]` |
| `floor` | opt string | `string` | `Optional[str]` |
| `hits` | opt integer, default 20, max 100 | `int64` | `Annotated[int, Meta(ge=1, le=100)]`, default 20 |
| `offset` | opt integer, default 1, max 50000 | `int64` | `Annotated[int, Meta(ge=1, le=50000)]`, default 1 |
| `sort` | opt string | `string` | `DMMItemListSort` enum, default `rank` |
| `keyword` | opt string | `string` | `Optional[str]` |
| `cid` | opt string | `string` (`ContentID`) | `Optional[str]` |
| `article[]` + `article_id[]` | opt, two parallel arrays | `string` (`Article`, `ArticleID`) | merged as `list[DMMItemListRequestParamsArticle]`, serialized expanded |
| `gte_date` / `lte_date` | opt, ISO8601 no timezone | `string` | `Annotated[Optional[datetime], Meta(tz=False)]` |
| `mono_stock` | opt string | `string` (`Stock`) | `DMMItemListMonoStock` enum (includes undocumented `dmp`) |

### Response — Pagination

| JSON Field | Official Docs | Official Go SDK (`ProductResponse`) | This Python SDK (`DMMItemListResponseBodyResult`) |
|------------|---------------|--------------------------------------|---------------------------------------------------|
| `result.status` | integer | | `_status: int \| str` → property `status: int` |
| `result.result_count` | integer | `int64` | `int` |
| `result.total_count` | integer | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `result.first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `result.items` | array | `[]Item` | `list[...]` (empty list when no results; key is never absent) |

### Response — Item (top-level)

| JSON Field | Official Docs | Official Go SDK (`Item`) | This Python SDK (`DMMItemListResponseBodyResultItem`) |
|------------|---------------|--------------------------|--------------------------------------------------------|
| `service_code` | string | `string` | `str` |
| `service_name` | string | `string` | `str` |
| `floor_code` | string | `string` | `str` |
| `floor_name` | string | `string` | `str` |
| `category_name` | string | `string` | `str` |
| `content_id` | string | `string` | `str` |
| `product_id` | string | `string` | `str` |
| `title` | string | `string` | `str` |
| `date` | string | `string` | `_date: str` → property `date: datetime` |
| `volume` | integer (JSON example is string) | `string` | `_volume: str` → property `volume: int` (handles both `"120"` and `"1:07:00"`) |
| `number` | integer | | `_number: str \| UnsetType` → property `number: Optional[int]` (type unverified) |
| `URL` | string | `string` | `url: str` (JSON name `URL`) |
| `affiliateURL` | string | `string` | `affiliate_url: str` (JSON name `affiliateURL`) |
| `review` | object | `ReviewInformation` (mapstructure zero value) | `DMMItemListResponseBodyResultItemReview \| UnsetType` |
| `imageURL` | object | `ImageURLList` | `image_url: DMMItemListResponseBodyResultItemImageURL` (JSON name `imageURL`) |
| `sampleImageURL` | object | `SampleImageURLList` (mapstructure zero value) | `sample_image_url: DMMItemListResponseBodyResultItemSampleImageURL \| UnsetType` (JSON name `sampleImageURL`) |
| `sampleMovieURL` | object | `SampleMovieURLList` (mapstructure zero value) | `sample_movie_url: DMMItemListResponseBodyResultItemSampleMovieURL \| UnsetType` (JSON name `sampleMovieURL`) |
| `tachiyomi` | object | | `DMMItemListResponseBodyResultItemTachiyomi \| UnsetType` |
| `prices` | object | `PriceInformation` | `price_info: DMMItemListResponseBodyResultItemPriceInfo` (JSON name `prices`) |
| `iteminfo` | object | `ItemInformation` | `item_info: DMMItemListResponseBodyResultItemItemInfo` (JSON name `iteminfo`) |
| `cdinfo` | object | `CdInformation` (mapstructure zero value) | `cd_info: DMMItemListResponseBodyResultItemCDInfo \| UnsetType` (JSON name `cdinfo`) |
| `jancode` | integer | `string` (mapstructure zero value) | `jan_code: str \| UnsetType` (JSON name `jancode`) |
| `isbn` | string | `string` (mapstructure zero value) | `str \| UnsetType` |
| `maker_product` | string | `string` (`ProductCode`) | `maker_product_code: str \| UnsetType` (JSON name `maker_product`) |
| `stock` | string | `string` (mapstructure zero value) | `str \| UnsetType` |
| `directory[]` | object array | | `_directories: list[...ItemInfoData] \| UnsetType` → property `directories: list[...]` (JSON name `directory`) |
| `campaign[]` | object array | | `_campaigns: list[...Campaign] \| UnsetType` → property `campaigns: list[...]` (JSON name `campaign`) |
| `URLsp` | undocumented | `string` (`URLMobile`) | `url_sp: str \| UnsetType` (JSON name `URLsp`) |
| `affiliateURLsp` | undocumented | `string` (`AffiliateURLMobile`) | `affiliate_url_sp: str \| UnsetType` (JSON name `affiliateURLsp`) |
| `comment` | undocumented | `string` (mapstructure zero value) | `str \| UnsetType` |
| `bandiInfo` | undocumented | `BandaiInformation` (`bandaiinfo`) | `bandai_info: DMMItemListResponseBodyResultItemBandaiInfo \| UnsetType` (JSON name `bandaiinfo`) |

### Response — review

| JSON Field | Official Docs | Official Go SDK (`ReviewInformation`) | This Python SDK (`DMMItemListResponseBodyResultItemReview`) |
|------------|---------------|---------------------------------------|--------------------------------------------------------------|
| `count` | integer | `int64` | `int` |
| `average` | float (JSON example is string) | `float64` (mapstructure auto-converts) | `_average: str` → property `average: float` |

### Response — imageURL

| JSON Field | Official Docs | Official Go SDK (`ImageURLList`) | This Python SDK (`DMMItemListResponseBodyResultItemImageURL`) |
|------------|---------------|----------------------------------|----------------------------------------------------------------|
| `list` | string | `string` | `str` |
| `small` | string | `string` | `str \| UnsetType` |
| `large` | string | `string` | `str \| UnsetType` |

### Response — sampleImageURL

| JSON Field | Official Docs | Official Go SDK (`SampleImageURLList`) | This Python SDK (`DMMItemListResponseBodyResultItemSampleImageURL`) |
|------------|---------------|----------------------------------------|-----------------------------------------------------------------------|
| `sample_s.image[]` | string array | `[]string` (`SmallSampleList.Image`) | property `sample_s_images` → `list[str]` |
| `sample_l.image[]` | string array | | property `sample_l_images` → `list[str]` |

### Response — sampleMovieURL

| JSON Field | Official Docs | Official Go SDK (`SampleMovieURLList`) | This Python SDK (`DMMItemListResponseBodyResultItemSampleMovieURL`) |
|------------|---------------|----------------------------------------|-----------------------------------------------------------------------|
| `size_476_306` | string | `string` | `str` |
| `size_560_360` | string | `string` | `str` |
| `size_644_414` | string | `string` | `str` |
| `size_720_480` | string | `string` | `str` |
| `pc_flag` | integer | `bool` (mapstructure auto-converts) | `_pc_flag: int` → property `pc_flag: bool` |
| `sp_flag` | integer | `bool` (mapstructure auto-converts) | `_sp_flag: int` → property `sp_flag: bool` |

### Response — prices

| JSON Field | Official Docs | Official Go SDK (`PriceInformation`) | This Python SDK (`DMMItemListResponseBodyResultItemPriceInfo`) |
|------------|---------------|---------------------------------------|------------------------------------------------------------------|
| `price` | string | `string` | `_price: str` → property `price_start_at: int` |
| `list_price` | string | `string` (`RetailPrice`) | `_list_price: str \| UnsetType` → property `list_price_start_at: Optional[int]` |
| `price_all` | undocumented | `string` | `_price_all: str \| UnsetType` → property `price_all_start_at: Optional[int]` (format unverified) |
| `deliveries` | object | `DistributionList` (`Distributions`) | `_deliveries: _DMMItemListResponseBodyResultItemPriceInfoDeliveries \| UnsetType` → property `deliveries: list[...]` |

### Response — prices.deliveries.delivery[]

| JSON Field | Official Docs | Official Go SDK (`Distribution`) | This Python SDK (`DMMItemListResponseBodyResultItemPriceInfoDelivery`) |
|------------|---------------|-----------------------------------|--------------------------------------------------------------------------|
| `type` | string | `string` | `str` |
| `price` | integer (JSON example is string) | `string` | `_price: str` → property `price: int` |
| `list_price` | undocumented | | `_list_price: str` → property `list_price: int` |

### Response — tachiyomi

| JSON Field | Official Docs | Official Go SDK | This Python SDK (`DMMItemListResponseBodyResultItemTachiyomi`) |
|------------|---------------|-----------------|------------------------------------------------------------------|
| `URL` | string | | `url: str` (JSON name `URL`) (type unverified) |
| `affiliateURL` | string (docs misspell as `affilaiteURL`) | | `affiliate_url: str` (JSON name `affiliateURL`) (type unverified) |

### Response — iteminfo

| JSON Field | Official Docs | Official Go SDK (`ItemInformation`) | This Python SDK (`DMMItemListResponseBodyResultItemItemInfo`) |
|------------|---------------|--------------------------------------|----------------------------------------------------------------|
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
| `keyword[]` | undocumented | `[]ItemComponent` | `_keyword: list[...ItemInfoData] \| UnsetType` → property `keywords: list[...]` |
| `artist[]` | undocumented | `[]ItemComponent` | `_artist: list[...ItemInfoDataWithRuby] \| UnsetType` → property `artists: list[...]` |
| `fighter[]` | undocumented | `[]ItemComponent` | `_fighter: list[...ItemInfoDataWithRuby] \| UnsetType` → property `fighters: list[...]` |

### Response — iteminfo[] (ItemComponent)

| JSON Field | Official Docs | Official Go SDK (`ItemComponent`) | This Python SDK |
|------------|---------------|-----------------------------------|-----------------|
| `id` | integer | `string` | `_id: int \| str` → property `id: str` (consider changing return type to `str \| None`) |
| `name` | string | `string` | `str` |
| `ruby` | string | | `str \| UnsetType` (`ItemInfoDataWithRuby` only; key may be absent) |

---

## 3. ActressSearch

### Request Params

| Field | Official Docs | Official Go SDK (`ActressService`) | This Python SDK (`DMMActressSearchRequestParams`) |
|-------|---------------|-------------------------------------|------------------------------------------------------|
| `initial` | opt string | `string` | `Optional[str]` |
| `actress_id` | opt integer | `string` (`ActressID`) | `Optional[str]` |
| `keyword` | opt string | `string` | `Optional[str]` |
| `gte_bust` / `lte_bust` | opt integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_waist` / `lte_waist` | opt integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_hip` / `lte_hip` | opt integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_height` / `lte_height` | opt integer | `string` | `Annotated[Optional[int], Meta(ge=0)]` |
| `gte_birthday` / `lte_birthday` | opt string (docs say `yyyymmdd`, example shows `1990-01-01`) | `string` | `Optional[date]` (ISO format) |
| `hits` | opt integer, default 20, max 100 | `int64` | `Annotated[int, Meta(ge=1, le=100)]`, default 20 |
| `offset` | opt integer, default 1 | `int64` | `Annotated[int, Meta(ge=1)]`, default 1 |
| `sort` | opt string, default `-name` | `string` | `Optional[DMMActressSearchSort]` (default `None`, not sent) |

> The official Go SDK `ActressService` (request) also contains `Bust`, `GteBust` ... `LteBirthday` etc., duplicating fields from the `Actress` response struct.

### Response — Pagination

| JSON Field | Official Docs | Official Go SDK (`ActressResponse`) | This Python SDK (`DMMActressSearchResponseBodyResult`) |
|------------|---------------|--------------------------------------|----------------------------------------------------------|
| `status` | integer (JSON example is string) | | `_status: int \| str` → property `status: int` |
| `result_count` | integer | `int64` | `int` |
| `total_count` | integer (JSON example is string) | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `actress[]` (container) | array | `[]Actress` (mapstructure zero value) | `_actress: list[...] \| UnsetType` → property `actresses: list[...]` (key absent when no results) |

### Response — Actress

| JSON Field | Official Docs | Official Go SDK (`Actress`) | This Python SDK (`DMMActressSearchResponseBodyResultActress`) |
|------------|---------------|-----------------------------|----------------------------------------------------------------|
| `id` | integer (JSON example is string) | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `bust` | integer (JSON example is string) | `string` (includes `GteBust` / `LteBust`, mixed with request params) | `_bust: Optional[str]` → property `bust: Optional[int]` |
| `waist` | integer (JSON example is string) | `string` (includes `GteWaist` / `LteWaist`, mixed with request params) | `_waist: Optional[str]` → property `waist: Optional[int]` |
| `hip` | integer (JSON example is string) | `string` (includes `GteHip` / `LteHip`, mixed with request params) | `_hip: Optional[str]` → property `hip: Optional[int]` |
| `height` | integer (JSON example is string or null) | `string` (includes `GteHeight` / `LteHeight`, mixed with request params) | `_height: Optional[str]` → property `height: Optional[int]` |
| `cup` | string | `string` (includes `GteCup` etc., mixed with request) | `str \| UnsetType` |
| `birthday` | string (JSON example has null) | `string` (`Birthday`, includes `GteBirthday` / `LteBirthday`) | `Optional[date]` |
| `blood_type` | string (JSON example has null) | `string` | `Optional[str]` |
| `hobby` | string (JSON example has null) | `string` | `Optional[str]` |
| `prefectures` | string (JSON example has null) | `string` | `Optional[str]` |
| `imageURL` (container) | object | `ActressImageList` | `image_url: DMMActressImageURL \| UnsetType` (JSON name `imageURL`) |
| `imageURL.small` | string | `string` | `str` |
| `imageURL.large` | string | `string` | `str` |
| `listURL` (container) | object | `ActressProductList` | `list_url: DMMActressListURL` (JSON name `listURL`) |
| `listURL.digital` | string | `string` | `str` |
| `listURL.monthly` | string | `string` | `str` |
| `listURL.mono` | string | `string` | `str` |
| `listURL.ppm` | undocumented | `string` (`Ppm`) | `ppm: str \| UnsetType` (presence unverified) |
| `listURL.rental` | undocumented | `string` (`Rental`) | `rental: str \| UnsetType` (presence unverified) |

---

## 4. GenreSearch / MakerSearch / SeriesSearch / AuthorSearch

### Request Params (shared)

| Field | Official Docs | Official Go SDK (`*Service`) | This Python SDK (`*RequestParams`) |
|-------|---------------|------------------------------|--------------------------------------|
| `floor_id` | req string | `string` | `str` |
| `initial` | opt string (AuthorSearch: prefix match, not initial letter) | `string` | `Optional[str]` |
| `hits` | opt integer, default 100, max 500 | `int64` | `Annotated[int, Meta(ge=1, le=500)]`, default 100 |
| `offset` | opt integer, default 1 | `int64` | `Annotated[int, Meta(ge=1)]`, default 1 |

### Response — Shared Pagination + Floor

| JSON Field | Official Docs | Official Go SDK (`*Response`) | This Python SDK (`DMMArticleSearchResponseBodyResultMixin`) |
|------------|---------------|-------------------------------|--------------------------------------------------------------|
| `status` | integer (JSON example is string) | | `_status: int \| str` → property `status: int` |
| `result_count` | integer | `int64` | `int` |
| `total_count` | integer (JSON example is string) | `int64` | `_total_count: int \| str` → property `total_count: int` |
| `first_position` | integer | `int64` | `_first_position: int \| str` → property `first_position: int` |
| `site_name` | string | `string` | `str` |
| `site_code` | string | `string` | `DMMSiteCode` |
| `service_name` | string | `string` | `str` |
| `service_code` | string | `string` | `str` |
| `floor_id` | integer (JSON example is string) | `string` | `str` |
| `floor_name` | string | `string` | `str` |
| `floor_code` | string | `string` | `str` |

### GenreSearch — genre[]

| JSON Field | Official Docs | Official Go SDK (`Genre`) | This Python SDK (`DMMGenreSearchResponseBodyResultGenre`) |
|------------|---------------|---------------------------|-------------------------------------------------------------|
| `genre[]` (container) | array | `[]Genre` (mapstructure zero value) | `_genre: list[...] \| UnsetType` → property `genres: list[...]` (key absent when no results) |
| `genre_id` | integer (JSON example is string) | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `list_url` | string | `string` | `str \| UnsetType` (absent on some floors) |

### MakerSearch — maker[]

| JSON Field | Official Docs | Official Go SDK (`Maker`) | This Python SDK (`DMMMakerSearchResponseBodyResultMaker`) |
|------------|---------------|---------------------------|-------------------------------------------------------------|
| `maker[]` (container) | array | `[]Maker` (mapstructure zero value) | `_maker: list[...] \| UnsetType` → property `makers: list[...]` (key absent when no results) |
| `maker_id` | integer (JSON example is string) | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `another_name` | undocumented | | `str \| UnsetType` |
| `list_url` | string | `string` | `str \| UnsetType` (absent on some floors) |

### SeriesSearch — series[]

| JSON Field | Official Docs | Official Go SDK (`Series`) | This Python SDK (`DMMSeriesSearchResponseBodyResultSeries`) |
|------------|---------------|----------------------------|--------------------------------------------------------------|
| `series[]` (container) | array | `[]Series` (mapstructure zero value) | `_series: list[...] \| UnsetType` → property `series: list[...]` (key absent when no results) |
| `series_id` | integer (JSON example is string) | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `list_url` | string | `string` | `str \| UnsetType` (absent on some floors) |

### AuthorSearch — author[]

| JSON Field | Official Docs | Official Go SDK (`Author`) | This Python SDK (`DMMAuthorSearchResponseBodyResultAuthor`) |
|------------|---------------|----------------------------|--------------------------------------------------------------|
| `author[]` (container) | array | `[]Author` (mapstructure zero value) | `_author: list[...] \| UnsetType` → property `authors: list[...]` (key absent when no results) |
| `author_id` | integer (JSON example is string) | `string` | `str` |
| `name` | string | `string` | `str` |
| `ruby` | string | `string` | `str` |
| `another_name` | string | | `str \| UnsetType` |
| `list_url` | string | `string` | `str \| UnsetType` (absent on some floors) |

---

## Known Issues in the Official Go SDK

| Issue | Field |
|-------|-------|
| `DMMFloor.ID` declared as `int64`; JSON is actually a string | `floor.id` |
| `ReviewInformation.Average` declared as `float64`; JSON is actually the string `"5.00"` | `review.average` |
| `SampleMovieURL.PCFlag` / `SPFlag` declared as `bool`; JSON is actually `0`/`1` | `sampleMovieURL.pc_flag` / `sp_flag` |
| `Actress` response struct mixes in `GteBust`, `LteBust` and other request param fields | `actress.*` |
| `SampleImageURLList` does not define `sample_l` | `sampleImageURL.sample_l` |
| `Distribution` does not define `list_price` | `prices.deliveries.delivery[].list_price` |
| `ItemComponent` does not define `ruby` | `iteminfo.actress[].ruby` etc. |
| `PriceInformation.PriceAll` is defined but not observed in live JSON | `prices.price_all` |
| `ActressProductList` defines `Ppm` and `Rental`; defined in this project but presence unverified | `listURL.ppm` / `listURL.rental` |
