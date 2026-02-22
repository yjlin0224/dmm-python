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

    _floor: list[DMMFloorListResponseBodyResultFloor] | msgspec.UnsetType = (
        msgspec.field(name="floor", default=msgspec.UNSET)
    )

    @property
    def floors(self) -> list[DMMFloorListResponseBodyResultFloor]:
        return self._floor if isinstance(self._floor, list) else []


class DMMFloorListResponseBodyResultSite(msgspec.Struct, kw_only=True, frozen=True):
    name: str
    code: DMMSiteCode

    _service: list[DMMFloorListResponseBodyResultService] | msgspec.UnsetType = (
        msgspec.field(name="service", default=msgspec.UNSET)
    )

    @property
    def services(self) -> list[DMMFloorListResponseBodyResultService]:
        return self._service if isinstance(self._service, list) else []


class DMMFloorListResponseBodyResult(msgspec.Struct, kw_only=True, frozen=True):
    _site: list[DMMFloorListResponseBodyResultSite] | msgspec.UnsetType = msgspec.field(
        name="site", default=msgspec.UNSET
    )

    @property
    def sites(self) -> list[DMMFloorListResponseBodyResultSite]:
        return self._site if isinstance(self._site, list) else []


class DMMFloorListResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMFloorListResponseBodyResult
