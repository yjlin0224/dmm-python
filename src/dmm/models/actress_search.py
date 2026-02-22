from datetime import date
from enum import StrEnum
from typing import Annotated, Optional

import msgspec

from dmm.utils import parse_int

from .base import DMMResponseBodyMixin, DMMResponseBodyResultPaginationMixin

__all__ = [
    "DMMActressSearchRequestParams",
    "DMMActressSearchSort",
    "DMMActressImageURL",
    "DMMActressListURL",
    "DMMActressSearchResponseBodyResultActress",
    "DMMActressSearchResponseBodyResult",
    "DMMActressSearchResponseBody",
]


class DMMActressSearchSort(StrEnum):
    NAME_ASC = "name"
    NAME_DESC = "-name"
    BUST_ASC = "bust"
    BUST_DESC = "-bust"
    WAIST_ASC = "waist"
    WAIST_DESC = "-waist"
    HIP_ASC = "hip"
    HIP_DESC = "-hip"
    HEIGHT_ASC = "height"
    HEIGHT_DESC = "-height"
    BIRTHDAY_ASC = "birthday"
    BIRTHDAY_DESC = "-birthday"
    ID_ASC = "id"
    ID_DESC = "-id"


class DMMActressSearchRequestParams(msgspec.Struct, kw_only=True):
    initial: Optional[str] = None
    actress_id: Optional[str] = None
    keyword: Optional[str] = None
    gte_bust: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    lte_bust: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    gte_waist: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    lte_waist: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    gte_hip: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    lte_hip: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    gte_height: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    lte_height: Annotated[Optional[int], msgspec.Meta(ge=0)] = None
    gte_birthday: Optional[date] = None
    lte_birthday: Optional[date] = None
    hits: Annotated[int, msgspec.Meta(ge=1, le=100)] = 20
    offset: Annotated[int, msgspec.Meta(ge=1)] = 1
    sort: Optional[DMMActressSearchSort] = None

    def __post_init__(self):
        if self.gte_bust is not None and self.lte_bust is not None:
            if self.gte_bust > self.lte_bust:
                raise ValueError("gte_bust must be less than lte_bust")
        if self.gte_waist is not None and self.lte_waist is not None:
            if self.gte_waist > self.lte_waist:
                raise ValueError("gte_waist must be less than lte_waist")
        if self.gte_hip is not None and self.lte_hip is not None:
            if self.gte_hip > self.lte_hip:
                raise ValueError("gte_hip must be less than lte_hip")
        if self.gte_height is not None and self.lte_height is not None:
            if self.gte_height > self.lte_height:
                raise ValueError("gte_height must be less than lte_height")
        if self.gte_birthday is not None and self.lte_birthday is not None:
            if self.gte_birthday > self.lte_birthday:
                raise ValueError("gte_birthday must be less than lte_birthday")


class DMMActressImageURL(msgspec.Struct, kw_only=True, frozen=True):
    small: str
    large: str


class DMMActressListURL(msgspec.Struct, kw_only=True, frozen=True):
    digital: str
    monthly: str
    mono: str


class DMMActressSearchResponseBodyResultActress(
    msgspec.Struct, kw_only=True, frozen=True
):
    id: str
    name: str
    ruby: str
    cup: str | msgspec.UnsetType = msgspec.UNSET
    birthday: Optional[date]
    blood_type: Optional[str]
    hobby: Optional[str]
    prefectures: Optional[str]
    image_url: DMMActressImageURL = msgspec.field(name="imageURL")
    list_url: DMMActressListURL = msgspec.field(name="listURL")

    _bust: Optional[str] = msgspec.field(name="bust", default=None)
    _waist: Optional[str] = msgspec.field(name="waist", default=None)
    _hip: Optional[str] = msgspec.field(name="hip", default=None)
    _height: Optional[str] = msgspec.field(name="height", default=None)

    @property
    def bust(self) -> Optional[int]:
        return parse_int(self._bust)

    @property
    def waist(self) -> Optional[int]:
        return parse_int(self._waist)

    @property
    def hip(self) -> Optional[int]:
        return parse_int(self._hip)

    @property
    def height(self) -> Optional[int]:
        return parse_int(self._height)


class DMMActressSearchResponseBodyResult(
    DMMResponseBodyResultPaginationMixin, kw_only=True, frozen=True
):
    _actress: list[DMMActressSearchResponseBodyResultActress] | msgspec.UnsetType = (
        msgspec.field(name="actress", default=msgspec.UNSET)
    )

    @property
    def actresses(self) -> list[DMMActressSearchResponseBodyResultActress]:
        return self._actress if isinstance(self._actress, list) else []


class DMMActressSearchResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMActressSearchResponseBodyResult
