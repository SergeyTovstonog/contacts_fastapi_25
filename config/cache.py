from typing import Callable, Optional, Tuple, Dict, Any

from fastapi_cache import FastAPICache
from starlette.requests import Request
from starlette.responses import Response

def custom_repo_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    # params = kwargs["args"]
    key_parts = [namespace, func.__name__] + [str(param) for param in args[1:]]
    return ":".join(key_parts)

async def invalidate_get_contacts_repo_cache(user_id: int):
    await FastAPICache.clear(namespace=f"get_contacts_repo:get_contacts:{user_id}:*")