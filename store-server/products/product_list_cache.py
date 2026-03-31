"""Кеш списка товаров каталога (Redis / default CACHES)."""

from django.conf import settings
from django.core.cache import cache

LIST_VERSION_KEY = "products:list:ver"


def _list_version() -> int:
    return int(cache.get_or_set(LIST_VERSION_KEY, 0, timeout=None))


def bump_product_list_cache() -> None:
    """Сбрасывает кеш списков при изменении товаров."""
    try:
        cache.incr(LIST_VERSION_KEY)
    except ValueError:
        cache.add(LIST_VERSION_KEY, 1, timeout=None)


def product_pks_cache_key(category_id: int | None) -> str:
    cat = str(category_id) if category_id is not None else "all"
    return f"products:pks:{_list_version()}:{cat}"


def cache_timeout() -> int:
    return int(settings.CACHES["default"].get("TIMEOUT") or 300)
