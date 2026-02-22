import re
from typing import Any, Final

import msgspec

from .models import (
    DMMActressSearchRequestParams,
    DMMAuthorSearchRequestParams,
    DMMFloorListRequestParams,
    DMMGenreSearchRequestParams,
    DMMItemListRequestParams,
    DMMMakerSearchRequestParams,
    DMMRequestData,
    DMMSeriesSearchRequestParams,
)
from .types import DMMHttpMethod


class DMMClient:
    BASE_URL: Final[str] = "https://api.dmm.com/affiliate/v3"
    AFFILIATE_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^.+-99\d$")

    def __init__(self, api_id: str, affiliate_id: str):
        self.__api_id = api_id.strip()
        self.__affiliate_id = affiliate_id.strip()

        if self.__api_id == "":
            raise ValueError("DMM API ID is required")
        if self.__affiliate_id == "":
            raise ValueError("DMM Affiliate ID is required")

        # https://affiliate.dmm.com/api/guide
        # アフィリエイトIDは末尾を990～999に設定してください。
        # 末尾が990～999以外ではエラーとなります。
        if not self.AFFILIATE_ID_PATTERN.match(self.__affiliate_id):
            raise ValueError("DMM Affiliate ID must end with '-990' ~ '-999'")

    @property
    def api_id(self) -> str:
        return self.__api_id

    @property
    def affiliate_id(self) -> str:
        return self.__affiliate_id

    def __create_request_data(
        self, method: DMMHttpMethod, path: str, params: msgspec.Struct
    ) -> DMMRequestData:
        params_dict: dict[str, Any] = msgspec.to_builtins(params)
        params_dict["api_id"] = self.api_id
        params_dict["affiliate_id"] = self.affiliate_id
        params_dict["output"] = "json"

        str_params_dict: dict[str, str] = {}
        for key, value in params_dict.items():
            if value is None:
                continue
            if (
                method == "GET"
                and path == "/ItemList"
                and key == "articles"
                and isinstance(value, list)
            ):
                if len(value) == 0:
                    continue
                if len(value) == 1:
                    str_params_dict[f"article"] = str(value[0]["type"])
                    str_params_dict[f"article_id"] = str(value[0]["id"])
                else:
                    for i, article in enumerate(value):
                        str_params_dict[f"article[{i}]"] = str(article["type"])
                        str_params_dict[f"article_id[{i}]"] = str(article["id"])
            else:
                str_params_dict[key] = str(value)

        return DMMRequestData(
            method=method, url=f"{self.BASE_URL}{path}", params=str_params_dict
        )

    def create_item_list_request_data(
        self, params: DMMItemListRequestParams
    ) -> DMMRequestData:
        return self.__create_request_data("GET", "/ItemList", params)

    def create_floor_list_request_data(
        self, params: DMMFloorListRequestParams
    ) -> DMMRequestData:
        return self.__create_request_data("GET", "/FloorList", params)

    def create_actress_search_request_data(
        self, params: DMMActressSearchRequestParams
    ) -> DMMRequestData:
        return self.__create_request_data("GET", "/ActressSearch", params)

    def create_genre_search_request_data(
        self, params: DMMGenreSearchRequestParams
    ) -> DMMRequestData:
        return self.__create_request_data("GET", "/GenreSearch", params)

    def create_maker_search_request_data(
        self, params: DMMMakerSearchRequestParams
    ) -> DMMRequestData:
        return self.__create_request_data("GET", "/MakerSearch", params)

    def create_series_search_request_data(
        self, params: DMMSeriesSearchRequestParams
    ) -> DMMRequestData:
        return self.__create_request_data("GET", "/SeriesSearch", params)

    def create_author_search_request_data(
        self, params: DMMAuthorSearchRequestParams
    ) -> DMMRequestData:
        return self.__create_request_data("GET", "/AuthorSearch", params)
