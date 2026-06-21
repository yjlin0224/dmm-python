import msgspec

from dmm.types import DMMSiteCode

from .base import DMMResponseBodyMixin

__all__ = [
    "DMMFloorListRequestParams",
    "DMMFloorListResponseBodyResultFloor",
    "DMMFloorListResponseBodyResultService",
    "DMMFloorListResponseBodyResultSite",
    "DMMFloorListResponseBodyResult",
    "DMMFloorListResponseBody",
]


class DMMFloorListRequestParams(msgspec.Struct, kw_only=True):
    pass


class DMMFloorListResponseBodyResultFloor(msgspec.Struct, kw_only=True, frozen=True):
    id: str
    name: str
    code: str


class DMMFloorListResponseBodyResultService(msgspec.Struct, kw_only=True, frozen=True):
    name: str
    code: str
    floors: list[DMMFloorListResponseBodyResultFloor] = msgspec.field(name="floor")


class DMMFloorListResponseBodyResultSite(msgspec.Struct, kw_only=True, frozen=True):
    name: str
    code: DMMSiteCode
    services: list[DMMFloorListResponseBodyResultService] = msgspec.field(
        name="service"
    )


class DMMFloorListResponseBodyResult(msgspec.Struct, kw_only=True, frozen=True):
    sites: list[DMMFloorListResponseBodyResultSite] = msgspec.field(name="site")


class DMMFloorListResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMFloorListResponseBodyResult
