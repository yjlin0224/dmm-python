from datetime import datetime
from enum import StrEnum
from typing import Annotated, Optional

import msgspec

from dmm.types import DMMSiteCode
from dmm.utils import parse_int

from .base import DMMResponseBodyMixin, DMMResponseBodyResultPaginationMixin

__all__ = [
    "DMMItemListSort",
    "DMMItemListArticleType",
    "DMMItemListMonoStock",
    "DMMItemListRequestParamsArticle",
    "DMMItemListRequestParams",
    "DMMItemListResponseBodyResultItemReview",
    "DMMItemListResponseBodyResultItemImageURL",
    "DMMItemListResponseBodyResultItemTachiyomi",
    "DMMItemListResponseBodyResultItemSampleImageURL",
    "DMMItemListResponseBodyResultItemSampleMovieURL",
    "DMMItemListResponseBodyResultItemPriceInfoDelivery",
    "DMMItemListResponseBodyResultItemPriceInfo",
    "DMMItemListResponseBodyResultItemItemInfoData",
    "DMMItemListResponseBodyResultItemItemInfoDataWithRuby",
    "DMMItemListResponseBodyResultItemItemInfo",
    "DMMItemListResponseBodyResultItemCDInfo",
    "DMMItemListResponseBodyResultItemCampaign",
    "DMMItemListResponseBodyResultItemBandaiInfo",
    "DMMItemListResponseBodyResultItem",
    "DMMItemListResponseBodyResult",
    "DMMItemListResponseBody",
]


class DMMItemListSort(StrEnum):
    RANK = "rank"
    PRICE_ASC = "price"
    PRICE_DESC = "-price"
    DATE = "date"
    REVIEW = "review"
    MATCH = "match"


class DMMItemListArticleType(StrEnum):
    ACTRESS = "actress"
    AUTHOR = "author"
    GENRE = "genre"
    SERIES = "series"
    MAKER = "maker"


class DMMItemListMonoStock(StrEnum):
    STOCK = "stock"
    RESERVE = "reserve"
    RESERVE_EMPTY = "reserve_empty"
    MONO = "mono"
    DMP = "dmp"


class DMMItemListRequestParamsArticle(msgspec.Struct, kw_only=True):
    type: DMMItemListArticleType
    id: str


class DMMItemListRequestParams(msgspec.Struct, kw_only=True):
    site: DMMSiteCode
    service: Optional[str] = None
    floor: Optional[str] = None
    hits: Annotated[int, msgspec.Meta(ge=1, le=100)] = 20
    offset: Annotated[int, msgspec.Meta(ge=1, le=50000)] = 1
    sort: DMMItemListSort = DMMItemListSort.RANK
    keyword: Optional[str] = None
    cid: Optional[str] = None
    articles: list[DMMItemListRequestParamsArticle] = []
    gte_date: Annotated[Optional[datetime], msgspec.Meta(tz=False)] = None
    lte_date: Annotated[Optional[datetime], msgspec.Meta(tz=False)] = None
    mono_stock: Optional[DMMItemListMonoStock] = None

    def __post_init__(self):
        if self.gte_date is not None and self.lte_date is not None:
            if self.gte_date > self.lte_date:
                raise ValueError("gte_date must be less than lte_date")


class DMMItemListResponseBodyResultItemReview(
    msgspec.Struct, kw_only=True, frozen=True
):
    count: int
    _average: str = msgspec.field(name="average")

    @property
    def average(self) -> float:
        return float(self._average)


class DMMItemListResponseBodyResultItemImageURL(
    msgspec.Struct, kw_only=True, frozen=True
):
    list: str
    small: str | msgspec.UnsetType = msgspec.UNSET
    large: str | msgspec.UnsetType = msgspec.UNSET


class DMMItemListResponseBodyResultItemTachiyomi(
    msgspec.Struct, kw_only=True, frozen=True
):
    url: str = msgspec.field(name="URL")  # [TODO] unsure
    affiliate_url: str = msgspec.field(name="affiliateURL")  # [TODO] unsure


class _DMMItemListResponseBodyResultItemSampleImageURLSample(
    msgspec.Struct, kw_only=True, frozen=True
):
    image: list[str]


class DMMItemListResponseBodyResultItemSampleImageURL(
    msgspec.Struct, kw_only=True, frozen=True
):
    _sample_s: (
        _DMMItemListResponseBodyResultItemSampleImageURLSample | msgspec.UnsetType
    ) = msgspec.field(name="sample_s", default=msgspec.UNSET)
    _sample_l: (
        _DMMItemListResponseBodyResultItemSampleImageURLSample | msgspec.UnsetType
    ) = msgspec.field(name="sample_l", default=msgspec.UNSET)

    @property
    def sample_s_images(self) -> list[str]:
        if isinstance(
            self._sample_s, _DMMItemListResponseBodyResultItemSampleImageURLSample
        ):
            return self._sample_s.image
        return []

    @property
    def sample_l_images(self) -> list[str]:
        if isinstance(
            self._sample_l, _DMMItemListResponseBodyResultItemSampleImageURLSample
        ):
            return self._sample_l.image
        return []


class DMMItemListResponseBodyResultItemSampleMovieURL(
    msgspec.Struct, kw_only=True, frozen=True
):
    size_476_306: str
    size_560_360: str
    size_644_414: str
    size_720_480: str

    _pc_flag: int = msgspec.field(name="pc_flag")
    _sp_flag: int = msgspec.field(name="sp_flag")

    @property
    def pc_flag(self) -> bool:
        return self._pc_flag >= 1

    @property
    def sp_flag(self) -> bool:
        return self._sp_flag >= 1


class DMMItemListResponseBodyResultItemPriceInfoDelivery(
    msgspec.Struct, kw_only=True, frozen=True
):
    type: str

    _price: str = msgspec.field(name="price")

    # undocumented fields
    _list_price: str = msgspec.field(name="list_price")

    @property
    def price(self) -> int:
        return int(self._price)

    @property
    def list_price(self) -> int:
        return int(self._list_price)


class _DMMItemListResponseBodyResultItemPriceInfoDeliveries(
    msgspec.Struct, kw_only=True, frozen=True
):
    delivery: list[DMMItemListResponseBodyResultItemPriceInfoDelivery]


class DMMItemListResponseBodyResultItemPriceInfo(
    msgspec.Struct, kw_only=True, frozen=True
):
    _price: str = msgspec.field(name="price")
    _list_price: str | msgspec.UnsetType = msgspec.field(
        name="list_price", default=msgspec.UNSET
    )
    _deliveries: (
        _DMMItemListResponseBodyResultItemPriceInfoDeliveries | msgspec.UnsetType
    ) = msgspec.field(name="deliveries", default=msgspec.UNSET)

    # undocumented fields
    _price_all: str | msgspec.UnsetType = msgspec.field(
        name="price_all", default=msgspec.UNSET
    )  # [TODO] unsure

    @property
    def price_start_at(self) -> int:
        return int(self._price.removesuffix("~"))

    @property
    def list_price_start_at(self) -> Optional[int]:
        if not isinstance(self._list_price, str):
            return None
        return int(self._list_price.removesuffix("~"))

    @property
    def price_all_start_at(self) -> Optional[int]:
        if not isinstance(self._price_all, str):
            return None
        return int(self._price_all.removesuffix("~"))

    @property
    def deliveries(self) -> list[DMMItemListResponseBodyResultItemPriceInfoDelivery]:
        if isinstance(
            self._deliveries, _DMMItemListResponseBodyResultItemPriceInfoDeliveries
        ):
            return self._deliveries.delivery
        return []


class DMMItemListResponseBodyResultItemItemInfoData(
    msgspec.Struct, kw_only=True, frozen=True
):
    name: str

    _id: int | str = msgspec.field(name="id")

    @property
    def id(self) -> str:
        # [TODO] API may return non-numeric strings (e.g. 'other'); consider returning str | None
        return str(self._id)


class DMMItemListResponseBodyResultItemItemInfoDataWithRuby(
    DMMItemListResponseBodyResultItemItemInfoData, kw_only=True, frozen=True
):
    ruby: str | msgspec.UnsetType = msgspec.UNSET


class DMMItemListResponseBodyResultItemItemInfo(
    msgspec.Struct, kw_only=True, frozen=True
):
    _genre: list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType = (
        msgspec.field(name="genre", default=msgspec.UNSET)
    )
    _series: list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType = (
        msgspec.field(name="series", default=msgspec.UNSET)
    )
    _maker: list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType = (
        msgspec.field(name="maker", default=msgspec.UNSET)
    )
    _actor: (
        list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby] | msgspec.UnsetType
    ) = msgspec.field(name="actor", default=msgspec.UNSET)
    _actress: (
        list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby] | msgspec.UnsetType
    ) = msgspec.field(name="actress", default=msgspec.UNSET)
    _director: (
        list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby] | msgspec.UnsetType
    ) = msgspec.field(name="director", default=msgspec.UNSET)
    _author: (
        list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby] | msgspec.UnsetType
    ) = msgspec.field(name="author", default=msgspec.UNSET)
    _label: list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType = (
        msgspec.field(name="label", default=msgspec.UNSET)
    )
    _type: list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType = (
        msgspec.field(name="type", default=msgspec.UNSET)
    )
    _color: list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType = (
        msgspec.field(name="color", default=msgspec.UNSET)
    )
    _size: list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType = (
        msgspec.field(name="size", default=msgspec.UNSET)
    )

    # undocumented fields
    _keyword: (
        list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType
    ) = msgspec.field(name="keyword", default=msgspec.UNSET)
    _artist: (
        list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby] | msgspec.UnsetType
    ) = msgspec.field(name="artist", default=msgspec.UNSET)
    _fighter: (
        list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby] | msgspec.UnsetType
    ) = msgspec.field(name="fighter", default=msgspec.UNSET)

    @property
    def genres(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._genre if isinstance(self._genre, list) else []

    @property
    def series(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._series if isinstance(self._series, list) else []

    @property
    def makers(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._maker if isinstance(self._maker, list) else []

    @property
    def actors(self) -> list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby]:
        return self._actor if isinstance(self._actor, list) else []

    @property
    def actresses(
        self,
    ) -> list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby]:
        return self._actress if isinstance(self._actress, list) else []

    @property
    def directors(
        self,
    ) -> list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby]:
        return self._director if isinstance(self._director, list) else []

    @property
    def authors(self) -> list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby]:
        return self._author if isinstance(self._author, list) else []

    @property
    def labels(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._label if isinstance(self._label, list) else []

    @property
    def types(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._type if isinstance(self._type, list) else []

    @property
    def colors(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._color if isinstance(self._color, list) else []

    @property
    def sizes(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._size if isinstance(self._size, list) else []

    @property
    def keywords(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._keyword if isinstance(self._keyword, list) else []

    @property
    def artists(self) -> list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby]:
        return self._artist if isinstance(self._artist, list) else []

    @property
    def fighters(
        self,
    ) -> list[DMMItemListResponseBodyResultItemItemInfoDataWithRuby]:
        return self._fighter if isinstance(self._fighter, list) else []


class DMMItemListResponseBodyResultItemCDInfo(
    msgspec.Struct, kw_only=True, frozen=True
):
    kind: str


class DMMItemListResponseBodyResultItemCampaign(
    msgspec.Struct, kw_only=True, frozen=True
):
    title: str

    _date_begin: str = msgspec.field(name="date_begin")
    _date_end: str = msgspec.field(name="date_end")

    @property
    def date_begin(self) -> datetime:
        return datetime.fromisoformat(self._date_begin)

    @property
    def date_end(self) -> datetime:
        return datetime.fromisoformat(self._date_end)


# undocumented
class DMMItemListResponseBodyResultItemBandaiInfo(
    msgspec.Struct, kw_only=True, frozen=True
):
    title_code: str = msgspec.field(name="titlecode")


class DMMItemListResponseBodyResultItem(msgspec.Struct, kw_only=True, frozen=True):
    service_code: str
    service_name: str
    floor_code: str
    floor_name: str
    category_name: str
    content_id: str
    product_id: str
    title: str
    review: DMMItemListResponseBodyResultItemReview | msgspec.UnsetType = msgspec.UNSET
    url: str = msgspec.field(name="URL")
    affiliate_url: str = msgspec.field(name="affiliateURL")
    image_url: DMMItemListResponseBodyResultItemImageURL = msgspec.field(
        name="imageURL"
    )
    tachiyomi: DMMItemListResponseBodyResultItemTachiyomi | msgspec.UnsetType = (
        msgspec.UNSET
    )
    sample_image_url: (
        DMMItemListResponseBodyResultItemSampleImageURL | msgspec.UnsetType
    ) = msgspec.field(name="sampleImageURL", default=msgspec.UNSET)
    sample_movie_url: (
        DMMItemListResponseBodyResultItemSampleMovieURL | msgspec.UnsetType
    ) = msgspec.field(name="sampleMovieURL", default=msgspec.UNSET)
    price_info: DMMItemListResponseBodyResultItemPriceInfo = msgspec.field(
        name="prices"
    )
    item_info: DMMItemListResponseBodyResultItemItemInfo = msgspec.field(
        name="iteminfo"
    )
    cd_info: DMMItemListResponseBodyResultItemCDInfo | msgspec.UnsetType = (
        msgspec.field(name="cdinfo", default=msgspec.UNSET)
    )
    jan_code: str | msgspec.UnsetType = msgspec.field(
        name="jancode", default=msgspec.UNSET
    )
    maker_product_code: str | msgspec.UnsetType = msgspec.field(
        name="maker_product", default=msgspec.UNSET
    )
    isbn: str | msgspec.UnsetType = msgspec.UNSET
    stock: str | msgspec.UnsetType = msgspec.UNSET

    # undocumented fields
    url_sp: str | msgspec.UnsetType = msgspec.field(name="URLsp", default=msgspec.UNSET)
    affiliate_url_sp: str | msgspec.UnsetType = msgspec.field(
        name="affiliateURLsp", default=msgspec.UNSET
    )
    comment: str | msgspec.UnsetType = msgspec.UNSET
    bandai_info: DMMItemListResponseBodyResultItemBandaiInfo | msgspec.UnsetType = (
        msgspec.field(name="bandaiinfo", default=msgspec.UNSET)
    )

    _date: str = msgspec.field(name="date")
    _volume: str = msgspec.field(name="volume")
    _number: str | msgspec.UnsetType = msgspec.field(  # [TODO] unsure
        name="number", default=msgspec.UNSET
    )
    _directories: (
        list[DMMItemListResponseBodyResultItemItemInfoData] | msgspec.UnsetType
    ) = msgspec.field(name="directory", default=msgspec.UNSET)
    _campaigns: list[DMMItemListResponseBodyResultItemCampaign] | msgspec.UnsetType = (
        msgspec.field(name="campaign", default=msgspec.UNSET)
    )

    @property
    def date(self) -> datetime:
        return datetime.fromisoformat(self._date)

    @property
    def volume(self) -> int:
        # "120" → 120 minutes; "1:07:00" (H:MM:SS) → 67 minutes
        v = self._volume
        if ":" in v:
            h, m, _ = v.split(":")
            return int(h) * 60 + int(m)
        return int(v)

    @property
    def number(self) -> Optional[int]:
        return parse_int(self._number)

    @property
    def directories(self) -> list[DMMItemListResponseBodyResultItemItemInfoData]:
        return self._directories if isinstance(self._directories, list) else []

    @property
    def campaigns(self) -> list[DMMItemListResponseBodyResultItemCampaign]:
        return self._campaigns if isinstance(self._campaigns, list) else []


class DMMItemListResponseBodyResult(
    DMMResponseBodyResultPaginationMixin, kw_only=True, frozen=True
):
    items: list[DMMItemListResponseBodyResultItem]


class DMMItemListResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMItemListResponseBodyResult
