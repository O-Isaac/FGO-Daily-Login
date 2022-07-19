import os
import traceback
from typing import List
import requests;
import time;
import json;
import subprocess;
import fgourl

from user import user, Bonus, Rewards, Login;

root_path = os.getcwd()
asset_bundle_json = os.path.join(root_path, "assetbundle.json")
asset_bundle_extractor = os.path.join(root_path, "Asset Bundle Extractor", "Asset Bundle Extractor.exe")

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
    subprocess.run([asset_bundle_extractor, '-a', assetbundle, '-r', fate_region])

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

        print(fgourl.asset_bundle_folder_)

        for i in range(userNums):
            try:
                instance = user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
            except Exception as ex:
                print(f'{i}th user login failed: {ex}')

def webhook_discord(data: list) -> None:
    endpoint = webhook_discord_url

    rewards: Rewards = data[0]
    login: Login = data[1]
    bonus: Bonus or str = data[2]    
    
    messageBonus = ''
    nl = '\n'

    if bonus != "No Bonus":
        messageBonus += f"__{bonus.message}__{nl}```{nl.join(bonus.items)}```"

        if bonus.bonus_name != None:
            messageBonus += f"{nl}__{bonus.bonus_name}__{nl}{bonus.bonus_detail}{nl}```{nl.join(bonus.bonus_camp_items)}```"
        
        messageBonus += "\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
            "title": "FGO Daily Bonus",
            "description": f"Scheluded Login Fate/Grand Order.\n\n{messageBonus}",
            "color": 563455,
            "fields": [
                {
                "name": "Level",
                "value": f"{rewards.level}",
                "inline": True
                },
                {
                "name": "Tickets",
                "value": f"{rewards.ticket}",
                "inline": True
                },
                {
                "name": "Saint Quartz",
                "value": f"{rewards.stone}",
                "inline": True
                },
                {
                "name": "Login Days",
                "value": f"{login.login_days}",
                "inline": True
                },
                {
                "name": "Total Days",
                "value": f"{login.total_days}",
                "inline": True
                },
                {
                "name": "Total Friend Points",
                "value": f"{login.total_fp}",
                "inline": True
                },
                {
                "name": "Friend Points",
                "value": f"+{login.add_fp}",
                "inline": True
                },
                {
                "name": "Ap Max",
                "value": f"{login.act_max}",
                "inline": True
                }
            ],
            "thumbnail": {
                "url": "https://grandorder.wiki/images/thumb/3/3d/Icon_Item_Saint_Quartz.png/200px-Icon_Item_Saint_Quartz.png"
            }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)


if __name__ == "__main__":
    main()