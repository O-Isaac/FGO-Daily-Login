import main
import requests
import user


def topLogin(data: list, region) -> None:
    endpoint = main.webhook_discord_url

    rewards: user.Rewards = data[0]
    login: user.Login = data[1]
    bonus: user.Bonus or str = data[2]

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
                "title": "FGO Daily Bonus - " + region,
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


def drawFP(servants, missions, region) -> None:
    endpoint = main.webhook_discord_url

    message_mission = ""
    message_servant = ""

    if (len(servants) > 0):
        servants_atlas = requests.get(
            f"https://api.atlasacademy.io/export/JP/basic_svt_lang_en.json").json()

        svt_dict = {svt["id"]: svt for svt in servants_atlas}

        for servant in servants:
            svt = svt_dict[servant.objectId]
            message_servant += f"`{svt['name']}` "

    if(len(missions) > 0):
        for mission in missions:
            message_mission += f"__{mission.message}__\n{mission.progressTo}/{mission.condition}\n"

    jsonData = {
        "content": None,
        "embeds": [
            {
                "title": "FGO Daily Bonus - " + region,
                "description": f"Scheluded Friend Point Fate/Grand Order.\n\n{message_mission}",
                "color": 5750876,
                "fields": [
                    {
                        "name": "Gacha Result",
                        "value": f"{message_servant}",
                        "inline": False
                    }
                ],
                "thumbnail": {
                    "url": "https://i.imgur.com/LJMPpP8.png"
                }
            }
        ],
        "attachments": []
    }

    headers = {
        "Content-Type": "application/json"
    }

    requests.post(endpoint, json=jsonData, headers=headers)
