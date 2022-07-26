"""The module for working with VK API."""

import vk

from sovabet.settings import (
    VK_ACCESS_TOKEN,
    VK_API_VERSION,
)


def get_vk_api():
    api = vk.API(access_token=VK_ACCESS_TOKEN, v=VK_API_VERSION)
    return api
