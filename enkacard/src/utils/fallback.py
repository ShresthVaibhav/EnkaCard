from __future__ import annotations

import logging
import re
from io import BytesIO

from PIL import Image

log = logging.getLogger("asset_fallback")

_SERIES = re.compile(r"(\d+)(\.\w+)(\?.*)?$")
_good: dict[str, Image.Image] = {}
_MAX = 300


def family(link: str) -> str:
    return _SERIES.sub(r"\2", link or "")


def first_of_series(link: str) -> str | None:
    match = _SERIES.search(link or "")
    if not match or int(match.group(1)) <= 1:
        return None
    digits = match.group(1)
    return link[: match.start(1)] + "1".zfill(len(digits)) + link[match.end(1):]


def remember(link: str, image: Image.Image) -> None:
    if len(_good) >= _MAX:
        _good.pop(next(iter(_good)))
    _good[family(link)] = image


def _open(data) -> Image.Image | None:
    try:
        return Image.open(BytesIO(data)).convert("RGBA")
    except Exception:
        return None


async def recover(link: str, download, size=None) -> Image.Image:
    alt = first_of_series(link)
    if alt:
        try:
            image = _open(await download(alt))
            if image is not None:
                log.info("asset %s missing, using %s", link, alt)
                remember(link, image)
                return image
        except Exception:
            pass
    image = _good.get(family(link))
    if image is not None:
        log.info("asset %s missing, reusing a similar one", link)
        return image.copy()
    log.info("asset %s missing, using a placeholder", link)
    return Image.new("RGBA", size or (256, 256), (0, 0, 0, 0))
