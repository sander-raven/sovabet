"""The module for working with VK API."""

from typing import Any

import vk

from sovabet.settings import (
    VK_ACCESS_TOKEN,
    VK_API_VERSION,
    VK_OWNER_ID,
)


def get_vk_api():
    api = vk.API(access_token=VK_ACCESS_TOKEN, v=VK_API_VERSION)
    return api


def get_comments(post_id: int) -> dict[str, Any] | None:
    api = get_vk_api()
    try:
        comments = api.wall.getComments(owner_id=VK_OWNER_ID, post_id=post_id)
    except:
        return None
    return comments
