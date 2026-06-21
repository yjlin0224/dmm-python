from enum import StrEnum
from typing import Literal, TypeAlias

DMMHttpMethod: TypeAlias = Literal["GET"]


class DMMSiteCode(StrEnum):
    DMM_COM = "DMM.com"
    FANZA = "FANZA"
