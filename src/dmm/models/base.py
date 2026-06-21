from typing import Any
from urllib.parse import urlencode

import msgspec

from dmm.types import DMMHttpMethod

__all__ = ["DMMRequestData", "DMMResponseBodyRequest"]


class DMMRequestData(msgspec.Struct, kw_only=True, frozen=True):
    method: DMMHttpMethod
    url: str
    params: dict[str, Any]

    @property
    def full_url(self) -> str:
        if len(self.params) == 0:
            return self.url
        query_string = urlencode(self.params)
        return f"{self.url}?{query_string}"

    def to_urllib_request(self, **kwargs: Any):
        from urllib.request import Request

        return Request(self.full_url, method=self.method, **kwargs)

    def to_requests_prepared_request(self, **kwargs: Any):
        try:
            from requests import Request
        except ImportError:
            raise ImportError("requests is not installed")

        return Request(
            method=self.method,
            url=self.url,
            params=self.params,
            **kwargs,
        ).prepare()

    def to_httpx_request(self, **kwargs: Any):
        try:
            from httpx import Request
        except ImportError:
            raise ImportError("httpx is not installed")

        return Request(
            method=self.method,
            url=self.url,
            params=self.params,
            **kwargs,
        )


class DMMResponseBodyResultPaginationMixin(msgspec.Struct, kw_only=True, frozen=True):
    result_count: int

    _status: int | str = msgspec.field(name="status")
    _first_position: int | str = msgspec.field(name="first_position")
    _total_count: int | str = msgspec.field(name="total_count")

    @property
    def status(self) -> int:
        return int(self._status)

    @property
    def first_position(self) -> int:
        return int(self._first_position)

    @property
    def total_count(self) -> int:
        return int(self._total_count)


class DMMResponseBodyRequest(msgspec.Struct, kw_only=True, frozen=True):
    parameters: dict[str, str]


class DMMResponseBodyMixin(msgspec.Struct, kw_only=True, frozen=True):
    request: DMMResponseBodyRequest
