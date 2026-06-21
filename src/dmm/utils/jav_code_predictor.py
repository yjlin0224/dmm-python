"""
Predict the JAV product code (番号) fields from an arbitrary input string.

Public API:
    predict_jav_code(input) -> JavCodePrediction
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# ---------------------------------------------------------------------------
# Internal constants
# ---------------------------------------------------------------------------

_VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".wmv", ".m4v", ".mpg", ".mov"}

_SOURCE_PREFIX_RE = re.compile(
    r"^(?:"
    r"\[[\w.\-]+\]@?"           # [44x.me]@ or [44x.me]
    r"|【[^】]+】"              # 【sex8.cc】 (fullwidth lenticular brackets)
    r"|[\w.\-]+@"               # hhd800.com@ or COSAV_MYS@
    r"|[a-z0-9]+\.[a-z]{2,4}-" # amav.xyz- (lowercase domain with TLD then dash)
    r")"
)
_QUALITY_TOKENS = re.compile(
    r"[-_](?:4k|8k|12000|fhd|hd|uhq|hq|\d+p|h264|h265)$",
    re.IGNORECASE,
)
_DOT_CODEC_RE = re.compile(r"\.(H265|H264|\d{3,4}p?)$", re.IGNORECASE)
_PART_SUFFIX_RE = re.compile(r"[-_]([A-Da-d]|\d)$")
_DATE_STUDIO_RE = re.compile(r"^\d{6}[-_]\d+[-_][\w][\w\-]*$", re.IGNORECASE)
_NHDTB_INTERNAL_RE = re.compile(r"^nhdtb-\d{5,}$", re.IGNORECASE)
_MAKER_CODE_RE = re.compile(r"^([A-Z0-9]+)-([A-Z]?\d+[A-Z]?)$", re.IGNORECASE)
_DELIVERY_CODE_RE = re.compile(r"^(\d+)?([a-z]{2,})(\d{3,})([a-z]?)$")
_NUMERIC_PREFIX_MAKER_RE = re.compile(r"^(\d+[A-Z]+\d*)-(\d+)$", re.IGNORECASE)
_FC2_RE = re.compile(r"^FC2-PPV-(\d+)$", re.IGNORECASE)
_TOKYO_HOT_RE = re.compile(r"^tokyo-hot-(.+)$", re.IGNORECASE)
_PAREN_MAKER_CODE_RE = re.compile(r"\(([A-Z0-9]+-[A-Z]?\d+[A-Z]?)\)", re.IGNORECASE)
_HJD_PREFIX_RE = re.compile(r"^[a-z0-9]+\.[a-z]{2,4}\d*", re.IGNORECASE)


class _ParsedType(str, Enum):
    MAKER_CODE = "maker_code"
    DELIVERY_CODE = "delivery_code"
    DATE_STUDIO = "date_studio"
    NHDTB_INTERNAL = "nhdtb_internal"
    JAPANESE_TITLE = "japanese_title"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Public result type
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class JavCodePrediction:
    parsed_type: str
    prefix: str
    number: str
    suffix: str
    maker_code: str
    cid: str
    split_part: str


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _has_cjk(s: str) -> bool:
    for c in s:
        cp = ord(c)
        if (0x3000 <= cp <= 0x9FFF
                or 0xF900 <= cp <= 0xFAFF
                or 0xFF00 <= cp <= 0xFFEF):
            return True
    return False


def _strip_source_prefix(name: str) -> str:
    result = _SOURCE_PREFIX_RE.sub("", name)
    if result != name:
        return result
    m = _HJD_PREFIX_RE.match(name)
    if m and m.end() < len(name):
        rest = name[m.end():]
        if re.match(r"[\da-zA-Z]", rest):
            return rest
    return name


def _strip_extension(name: str) -> str:
    p = Path(name)
    if p.suffix.lower() in _VIDEO_EXTENSIONS:
        stem = _DOT_CODEC_RE.sub("", p.stem)
        return stem
    return name


def _strip_quality_suffixes(name: str) -> str:
    prev = None
    while prev != name:
        prev = name
        name = _QUALITY_TOKENS.sub("", name)
    return name


def _strip_noise_suffixes(name: str) -> str:
    name = re.sub(r"-uncensored.*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"([A-Z0-9\-]+\d)[　-鿿豈-﫿＀-￯].*$", r"\1", name, flags=re.IGNORECASE)
    name = re.sub(r"([A-Z0-9\-]+\d)\s+[　-鿿豈-﫿＀-￯].*$", r"\1", name, flags=re.IGNORECASE)
    name = re.sub(r"_?\[4K\]$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"^([A-Z0-9]*[A-Z][A-Z0-9]*-[A-Z]?\d+[A-Z]?)-[A-Za-z]{2,}.*$", r"\1", name, flags=re.IGNORECASE)
    name = re.sub(r"\.[a-z]{2,4}$", "", name, flags=re.IGNORECASE)
    return name.rstrip(" .,")


def _strip_part_suffix(name: str) -> tuple[str, str]:
    m = _PART_SUFFIX_RE.search(name)
    if m:
        part = m.group(1)
        stripped = name[: m.start()]
        if not re.search(r"\d$", stripped):
            return name, ""
        if part == "0":
            return stripped, ""
        return stripped, part
    return name, ""


def _delivery_display_prefix(raw: str) -> str:
    if raw.startswith("h_"):
        return re.sub(r"^h_\d+", "", raw).upper()
    m = re.match(r"^(\d+)([a-z].*)$", raw)
    if m:
        num_part, letter_part = m.group(1), m.group(2)
        if letter_part.startswith("d") and num_part.endswith("3"):
            return ("3" + letter_part).upper()
        return letter_part.upper()
    return raw.upper()


def _part_to_letter(part: str) -> str:
    if not part:
        return ""
    if part.upper() in "ABCDEFGHIJ":
        return part.upper()
    try:
        n = int(part)
        return chr(ord("A") + n - 1) if n != 0 else ""
    except ValueError:
        return part.upper()


def _part_to_num(part: str) -> str:
    if not part:
        return ""
    if len(part) == 1 and part.upper().isalpha():
        return str(ord(part.upper()) - ord("A") + 1)
    try:
        n = int(part)
        return str(n) if n != 0 else ""
    except ValueError:
        return part


def _parse_core(core: str) -> tuple[_ParsedType, str, str, str]:
    """Return (type, prefix, number, suffix). All internal logic lives here."""
    # FC2-PPV
    m = _FC2_RE.match(core)
    if m:
        return _ParsedType.MAKER_CODE, "FC2-PPV", m.group(1), ""

    # Tokyo-Hot: embedded quality+part suffix stripped into suffix field
    m = _TOKYO_HOT_RE.match(core)
    if m:
        number = m.group(1)
        pm = re.search(r"[-_](?:fhd|uhq|hd|4k|8k)\s*(\d+)$", number, re.IGNORECASE)
        part_str = ""
        if pm:
            part_str = pm.group(1)
            number = number[:pm.start()]
        return _ParsedType.MAKER_CODE, "Tokyo-Hot", number.upper(), part_str

    # Date-studio: YYMMDD_NNN-STUDIO
    if _DATE_STUDIO_RE.match(core):
        m2 = re.match(r"^(\d{6}[-_]\d+)[-_](\w+)(?:[-_].*)?$", core, re.IGNORECASE)
        if m2:
            return _ParsedType.DATE_STUDIO, "", m2.group(1), m2.group(2).upper()
        return _ParsedType.DATE_STUDIO, "", "", ""

    # NHDTB internal: nhdtb-79001 → episode=790, part=01
    if _NHDTB_INTERNAL_RE.match(core):
        nm = re.match(r"^nhdtb-(\d+?)(\d{2})$", core, re.IGNORECASE)
        if nm:
            return _ParsedType.NHDTB_INTERNAL, "NHDTB", nm.group(1), nm.group(2)
        return _ParsedType.NHDTB_INTERNAL, "NHDTB", "", ""

    # Maker code in parentheses: (md-0302)
    pm2 = _PAREN_MAKER_CODE_RE.search(core)
    if pm2:
        inner = pm2.group(1).upper()
        mm = _MAKER_CODE_RE.match(inner)
        if mm:
            return _ParsedType.MAKER_CODE, mm.group(1), mm.group(2), ""

    # Pure CJK title
    if _has_cjk(core) and not re.search(r"[A-Z0-9]-[A-Z]?\d", core, re.IGNORECASE):
        return _ParsedType.JAPANESE_TITLE, "", "", ""

    # Numeric-prefix maker code: 390JAC-219
    m = _NUMERIC_PREFIX_MAKER_RE.match(core)
    if m:
        return _ParsedType.MAKER_CODE, m.group(1).upper(), m.group(2), ""

    # Standard maker code
    m = _MAKER_CODE_RE.match(core)
    if m:
        prefix = m.group(1).upper()
        num_raw = m.group(2).upper()
        return _ParsedType.MAKER_CODE, prefix, num_raw, ""

    # All-uppercase no-hyphen: SCOP171 → SCOP / 171
    m = re.match(r"^([A-Z]{2,})(\d+[A-Z]?)$", core)
    if m:
        return _ParsedType.MAKER_CODE, m.group(1), m.group(2), ""

    # h_ vendor prefix delivery code
    if core.lower().startswith("h_"):
        rest = core[2:]
        m = re.match(r"^(\d+)?([a-z]+)(\d{3,})([a-z]?)$", rest.lower())
        if m:
            vendor = "h_" + (m.group(1) or "")
            return _ParsedType.DELIVERY_CODE, vendor + m.group(2), m.group(3), m.group(4)

    # 配信品番
    m = _DELIVERY_CODE_RE.match(core.lower())
    if m:
        return _ParsedType.DELIVERY_CODE, (m.group(1) or "") + m.group(2), m.group(3), m.group(4)

    return _ParsedType.UNKNOWN, "", "", ""


def _build_maker_code(ptype: _ParsedType, prefix: str, number: str, suffix: str) -> str:
    if ptype == _ParsedType.MAKER_CODE:
        sep = "_" if prefix == "Tokyo-Hot" else "-"
        return f"{prefix}{sep}{number}{suffix}"
    if ptype == _ParsedType.DELIVERY_CODE:
        num_display = number.lstrip("0") or "0"
        if len(num_display) < 3:
            num_display = num_display.zfill(3)
        return f"{_delivery_display_prefix(prefix)}-{num_display}"
    if ptype == _ParsedType.DATE_STUDIO:
        return f"{number}-{suffix}" if suffix else number
    return ""


def _build_cid(ptype: _ParsedType, number: str, after_part: str) -> str:
    if ptype == _ParsedType.DELIVERY_CODE:
        return after_part
    if ptype == _ParsedType.DATE_STUDIO:
        return number
    return ""


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def predict_jav_code(input: str) -> JavCodePrediction:
    """Predict the JAV product code fields from an arbitrary input string.

    Returns a JavCodePrediction with parsed_type, prefix, number, suffix,
    maker_code, cid, and split_part. filename and keyword are intentionally
    excluded — derive them from the result fields as needed.
    """
    after_source = _strip_source_prefix(input)
    after_ext = _strip_extension(after_source)
    after_quality = _strip_noise_suffixes(after_ext)
    after_quality = _strip_quality_suffixes(after_quality)
    after_part, part = _strip_part_suffix(after_quality)

    ptype, prefix, number, suffix = _parse_core(after_part)

    # NHDTB: embedded part in suffix → promote to maker_code
    if ptype == _ParsedType.NHDTB_INTERNAL and number:
        ptype = _ParsedType.MAKER_CODE
        part = _part_to_letter(suffix) or part
        suffix = ""

    # Tokyo-Hot: embedded part in suffix → move to part
    if ptype == _ParsedType.MAKER_CODE and prefix == "Tokyo-Hot" and suffix:
        part = _part_to_letter(suffix) or part
        suffix = ""

    # Trailing A-D on number = part indicator (except hhd800.com@ source)
    if (ptype == _ParsedType.MAKER_CODE
            and re.match(r".*\d[A-D]$", number)
            and not input.lower().startswith("hhd800.com@")):
        part = number[-1]
        number = number[:-1]

    # Normalise delivery_code prefix to display form
    if ptype == _ParsedType.DELIVERY_CODE:
        prefix = _delivery_display_prefix(prefix)

    split_part = _part_to_num(part)
    maker_code = _build_maker_code(ptype, prefix, number, suffix)
    cid = _build_cid(ptype, number, after_part)

    return JavCodePrediction(
        parsed_type=ptype.value,
        prefix=prefix,
        number=number,
        suffix=suffix,
        maker_code=maker_code,
        cid=cid,
        split_part=split_part,
    )
