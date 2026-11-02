from contextvars import ContextVar
from io import BytesIO
from PIL import Image

_img: ContextVar = ContextVar('namecard_bg', default=None)

_enabled: bool = False

_nc_cache: dict[int, Image.Image | None] = {}

_url_cache: dict[int, str | None] = {}
_assets = None


def set_namecard_bg(img: Image.Image | None) -> None:
    _img.set(img)


def get_namecard_bg() -> Image.Image | None:
    return _img.get()


def clear_namecard_bg() -> None:
    _img.set(None)


def enable_namecard_mode() -> None:
    global _enabled
    _enabled = True


def disable_namecard_mode() -> None:
    global _enabled
    _enabled = False


def is_namecard_enabled() -> bool:
    return _enabled


def clear_nc_cache() -> None:
    _nc_cache.clear()


def _get_nc_url(char_id: int) -> str | None:
    global _assets
    if char_id in _url_cache:
        return _url_cache[char_id]
    try:
        if _assets is None:
            from enkanetwork import Assets
            _assets = Assets()
        char = _assets.DATA["characters"].get(str(char_id), {})
        internal = char.get("iconName", "").replace("UI_AvatarIcon_", "")
        for nc_id, nc_data in _assets.DATA.get("namecards", {}).items():
            if nc_data.get("icon") == f"UI_NameCardIcon_{internal}":
                nc_obj = _assets.namecards(int(nc_id))
                url = nc_obj.banner.url if nc_obj else None
                _url_cache[char_id] = url
                return url
        _url_cache[char_id] = None
    except Exception:
        _url_cache[char_id] = None
    return None


async def fetch_and_set_for_char(char_id: int) -> None:
    if not _enabled:
        return
    if char_id in _nc_cache:
        nc = _nc_cache[char_id]
        if nc is not None:
            set_namecard_bg(nc)
        return
    url = _get_nc_url(char_id)
    if not url:
        _nc_cache[char_id] = None
        return
    try:
        from curl_cffi.requests import AsyncSession
        async with AsyncSession(impersonate="chrome124") as s:
            r = await s.get(url)
        nc = Image.open(BytesIO(r.content)).convert("RGBA")
        _nc_cache[char_id] = nc
        set_namecard_bg(nc)
    except Exception:
        _nc_cache[char_id] = None


def nc_cover(nc: Image.Image, w: int, h: int) -> Image.Image:
    nw, nh = nc.size
    scale = max(w / nw, h / nh)
    new_w = int(nw * scale)
    new_h = int(nh * scale)
    scaled = nc.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return scaled.crop((left, top, left + w, top + h)).convert("RGBA")
