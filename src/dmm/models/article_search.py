from typing import Annotated, Optional

import msgspec

from dmm.types import DMMSiteCode

from .base import DMMResponseBodyMixin, DMMResponseBodyResultPaginationMixin

__all__ = [
    "DMMGenreSearchRequestParams",
    "DMMMakerSearchRequestParams",
    "DMMSeriesSearchRequestParams",
    "DMMAuthorSearchRequestParams",
    "DMMGenreSearchResponseBodyResultGenre",
    "DMMMakerSearchResponseBodyResultMaker",
    "DMMSeriesSearchResponseBodyResultSeries",
    "DMMAuthorSearchResponseBodyResultAuthor",
    "DMMGenreSearchResponseBodyResult",
    "DMMMakerSearchResponseBodyResult",
    "DMMSeriesSearchResponseBodyResult",
    "DMMAuthorSearchResponseBodyResult",
    "DMMGenreSearchResponseBody",
    "DMMMakerSearchResponseBody",
    "DMMSeriesSearchResponseBody",
    "DMMAuthorSearchResponseBody",
]


class DMMArticleSearchRequestParamsMixin(msgspec.Struct, kw_only=True):
    floor_id: str
    initial: Optional[str] = None
    hits: Annotated[int, msgspec.Meta(ge=1, le=500)] = 100
    offset: Annotated[int, msgspec.Meta(ge=1)] = 1


class DMMGenreSearchRequestParams(DMMArticleSearchRequestParamsMixin, kw_only=True):
    pass


class DMMMakerSearchRequestParams(DMMArticleSearchRequestParamsMixin, kw_only=True):
    pass


class DMMSeriesSearchRequestParams(DMMArticleSearchRequestParamsMixin, kw_only=True):
    pass


class DMMAuthorSearchRequestParams(DMMArticleSearchRequestParamsMixin, kw_only=True):
    pass


class DMMArticleSearchResponseBodyResultArticleMixin(
    msgspec.Struct, kw_only=True, frozen=True
):
    name: str
    ruby: str
    list_url: str


class DMMGenreSearchResponseBodyResultGenre(
    DMMArticleSearchResponseBodyResultArticleMixin, kw_only=True, frozen=True
):
    genre_id: str


class DMMMakerSearchResponseBodyResultMaker(
    DMMArticleSearchResponseBodyResultArticleMixin, kw_only=True, frozen=True
):
    maker_id: str


class DMMSeriesSearchResponseBodyResultSeries(
    DMMArticleSearchResponseBodyResultArticleMixin, kw_only=True, frozen=True
):
    series_id: str


class DMMAuthorSearchResponseBodyResultAuthor(
    DMMArticleSearchResponseBodyResultArticleMixin, kw_only=True, frozen=True
):
    author_id: str
    another_name: str | msgspec.UnsetType = msgspec.UNSET


class DMMArticleSearchResponseBodyResultMixin(
    DMMResponseBodyResultPaginationMixin, kw_only=True, frozen=True
):
    site_name: str
    site_code: DMMSiteCode
    service_name: str
    service_code: str
    floor_id: str
    floor_name: str
    floor_code: str


class DMMGenreSearchResponseBodyResult(
    DMMArticleSearchResponseBodyResultMixin, kw_only=True, frozen=True
):
    _genre: list[DMMGenreSearchResponseBodyResultGenre] | msgspec.UnsetType = (
        msgspec.field(name="genre", default=msgspec.UNSET)
    )

    @property
    def genres(self) -> list[DMMGenreSearchResponseBodyResultGenre]:
        return self._genre if isinstance(self._genre, list) else []


class DMMMakerSearchResponseBodyResult(
    DMMArticleSearchResponseBodyResultMixin, kw_only=True, frozen=True
):
    _maker: list[DMMMakerSearchResponseBodyResultMaker] | msgspec.UnsetType = (
        msgspec.field(name="maker", default=msgspec.UNSET)
    )

    @property
    def makers(self) -> list[DMMMakerSearchResponseBodyResultMaker]:
        return self._maker if isinstance(self._maker, list) else []


class DMMSeriesSearchResponseBodyResult(
    DMMArticleSearchResponseBodyResultMixin, kw_only=True, frozen=True
):
    _series: list[DMMSeriesSearchResponseBodyResultSeries] | msgspec.UnsetType = (
        msgspec.field(name="series", default=msgspec.UNSET)
    )

    @property
    def series(self) -> list[DMMSeriesSearchResponseBodyResultSeries]:
        return self._series if isinstance(self._series, list) else []


class DMMAuthorSearchResponseBodyResult(
    DMMArticleSearchResponseBodyResultMixin, kw_only=True, frozen=True
):
    _author: list[DMMAuthorSearchResponseBodyResultAuthor] | msgspec.UnsetType = (
        msgspec.field(name="author", default=msgspec.UNSET)
    )

    @property
    def authors(self) -> list[DMMAuthorSearchResponseBodyResultAuthor]:
        return self._author if isinstance(self._author, list) else []


class DMMGenreSearchResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMGenreSearchResponseBodyResult


class DMMMakerSearchResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMMakerSearchResponseBodyResult


class DMMSeriesSearchResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMSeriesSearchResponseBodyResult


class DMMAuthorSearchResponseBody(DMMResponseBodyMixin, kw_only=True, frozen=True):
    result: DMMAuthorSearchResponseBodyResult
