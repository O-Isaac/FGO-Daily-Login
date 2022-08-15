import os
import requests
import time
import json
import subprocess
import fgourl
import user

root_path = os.getcwd()
asset_bundle_json = os.path.join(root_path, "assetbundle.json")
asset_bundle_extractor = os.path.join(
    root_path, "Asset Bundle Extractor", "Asset Bundle Extractor.exe")

# Enviroments Variables
userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
fate_region = os.environ['fateRegion']
webhook_discord_url = os.environ['webhookDiscord']
UA = os.environ['UserAgent']

if UA != 'nullvalue':
    fgourl.user_agent_ = UA

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)


def get_assets_json(assetbundle):
    subprocess.run([asset_bundle_extractor, '-a',
                    assetbundle, '-r', fate_region])


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
        fgourl.set_latest_assets()

        for i in range(userNums):
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                instance.drawFP()
                time.sleep(2)
            except Exception as ex:
                print(f'{i}th user login failed: {ex}')


if __name__ == "__main__":
    main()
