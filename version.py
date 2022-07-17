# Thanks to atlas academy for this script!
# All credits to atlas
# Github: github.com/atlasacademy
# Website: atlasacademy.io
# Api: api.atlasacademy.io
# Apps: apps.atlasacademy.io

import re
import time

import json5
import httpx
import lxml.html

PLAY_STORE_URL = {
    "NA": "https://play.google.com/store/apps/details?id=com.aniplex.fategrandorder.en",
    "JP": "https://play.google.com/store/apps/details?id=com.aniplex.fategrandorder",
    "KR": "https://play.google.com/store/apps/details?id=com.netmarble.fgok",
    "TW": "https://play.google.com/store/apps/details?id=com.xiaomeng.fategrandorder",
}

APP_STORE_URL = {
    "NA": "http://itunes.apple.com/us/lookup?bundleId=com.aniplex.fategrandorder.en",
    "CN": "http://itunes.apple.com/cn/lookup?bundleId=com.bilibili.fatego",
    "JP": "http://itunes.apple.com/jp/lookup?bundleId=com.aniplex.fategrandorder",
    "KR": "http://itunes.apple.com/kr/lookup?bundleId=com.netmarble.fgok",
    "TW": "http://itunes.apple.com/tw/lookup?bundleId=com.xiaomeng.fategrandorder",
}

PLAY_STORE_XPATH_1 = "/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[4]/div[1]/div[2]/div/div[4]/span/div/span"
PLAY_STORE_XPATH_2 = "/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/c-wiz[3]/div[1]/div[2]/div/div[4]/span/div/span"
PLAY_STORE_XPATH_3 = '//div[div[text()="Current Version"]]/span/div/span/text()'
VERSION_REGEX = re.compile(r"^\d+\.\d+\.\d+$")


def get_CN_android_version():
    r = httpx.get("https://static.biligame.com/config/fgo.config.js")
    if match := re.search(r"\"latest_version\": \"(.*)\"", r.text):
        if VERSION_REGEX.match(match.group(1)):
            return match.group(1)

    return None


def get_play_store_ver(region: str):
    if region == "CN":
        return get_CN_android_version()

    play_store_response = httpx.get(PLAY_STORE_URL[region], follow_redirects=True)
    play_store_html = lxml.html.fromstring(play_store_response.text)

    for xpath in (PLAY_STORE_XPATH_1, PLAY_STORE_XPATH_2, PLAY_STORE_XPATH_3):
        try:
            xpath_version: str = play_store_html.xpath(xpath)[0].text
            if VERSION_REGEX.match(xpath_version):
                return xpath_version
        except:  # pylint: disable=bare-except
            continue

    for match in re.finditer(
        r"<script nonce=\"\S+\">AF_initDataCallback\((.*?)\);",
        play_store_response.text,
    ):
        try:
            data = json5.loads(match.group(1))
            if (
                "data" in data
                and len(data["data"]) > 2
                and isinstance(data["data"][1], str)
                and VERSION_REGEX.match(data["data"][1])
            ):
                return data["data"][1]

            deep_version = data["data"][1][2][140][0][0][0]
            if isinstance(deep_version, str) and VERSION_REGEX.match(deep_version):
                return deep_version

        except:  # pylint: disable=bare-except
            pass

    return None


def get_app_store_ver(region: str):
    r = httpx.get(APP_STORE_URL[region] + f"&t={int(time.time())}")
    app_store_version: str = r.json()["results"][0]["version"]
    if VERSION_REGEX.match(app_store_version):
        return app_store_version

    return None


def get_version(region: str) -> None:
    if region not in APP_STORE_URL:
        return None

    play_store_version = get_play_store_ver(region)
    if play_store_version is not None:
        return play_store_version

    app_store_version = get_app_store_ver(region)
    if app_store_version is not None:
        return app_store_version