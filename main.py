import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

from datetime import datetime
from croniter import croniter

# Enviroments Variables
userIds = os.environ.get("userIds").split(',')
authKeys = os.environ.get("authKeys").split(',')
secretKeys = os.environ.get("secretKeys").split(',')
fate_region = os.environ.get("fateRegion")
webhook_discord_url = os.environ.get("webhookDiscord")
blue_apple_cron = os.environ.get("MAKE_BLUE_APPLE")

UA = os.environ.get("UserAgent")

if UA:
    fgourl.user_agent_ = UA

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')


def check_blue_apple_cron(instance):
    if blue_apple_cron:

        cron = croniter(blue_apple_cron)
        next_date = cron.get_next(datetime)
        current_date = datetime.now()
        
        if current_date >= next_date:
            logger.info('Trying buy one blue apple!')
            instance.buyBlueApple(1)
            time.sleep(2)


def get_latest_verCode():
    endpoint = ""

    if fate_region == "NA":
        endpoint += "https://raw.githubusercontent.com/O-Isaac/FGO-VerCode-extractor/NA/VerCode.json"
    else:
        endpoint += "https://raw.githubusercontent.com/O-Isaac/FGO-VerCode-extractor/JP/VerCode.json"

    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']


def main():
    if userNums == authKeyNums and userNums == secretKeyNums:
        logger.info('Getting Lastest Assets Info')
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                logger.info('Loggin into account!')
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                logger.info('Throw daily friend summon!')
                instance.drawFP()
                time.sleep(2)
                check_blue_apple_cron(instance)
            except Exception as ex:
                logger.error(ex)


if __name__ == "__main__":
    main()
