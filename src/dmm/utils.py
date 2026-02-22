from typing import Optional

import msgspec


def parse_int(value: Optional[str] | msgspec.UnsetType) -> Optional[int]:
    if not isinstance(value, str) or (v := value.strip()) == "":
        return None
    return int(v)
