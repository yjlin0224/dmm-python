from enum import StrEnum
from typing import Literal

type DMMHttpMethod = Literal["GET"]


class DMMSiteCode(StrEnum):
    DMM_COM = "DMM.com"
    FANZA = "FANZA"
