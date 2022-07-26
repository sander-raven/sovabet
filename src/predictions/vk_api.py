"""The module for working with VK API."""

from typing import Any, Iterable

import vk
from vk.exceptions import VkAPIError

from sovabet.settings import (
    VK_ACCESS_TOKEN,
    VK_API_VERSION,
    VK_OWNER_ID,
)


def get_vk_api():
    api = vk.API(access_token=VK_ACCESS_TOKEN, v=VK_API_VERSION)
    return api


def get_comments(
    post_id: int, api: vk.API = None, extended: bool = True
) -> dict[str, Any] | None:
    if api is None:
        api = get_vk_api()
    try:
        if extended:
            response = api.wall.getComments(
                owner_id=VK_OWNER_ID,
                post_id=post_id,
                count=100,
                lang="ru",
                extended=1,
                fields="first_name,last_name",
            )
        else:
            response = api.wall.getComments(
                owner_id=VK_OWNER_ID,
                post_id=post_id,
                count=100,
                lang="ru",
            )
    except VkAPIError:
        return None
    return response


def get_users(
    user_ids: Iterable[int], api: vk.API = None
) -> list[dict[str, Any]] | None:
    if api is None:
        api = get_vk_api()
    try:
        users = api.users.get(user_ids=user_ids, lang="ru")
    except VkAPIError:
        return None
    return users
