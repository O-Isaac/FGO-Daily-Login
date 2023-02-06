# coding: utf-8
import uuid
import hashlib
import base64
import fgourl
import mytime
import gacha
import webhook
import main

from urllib.parse import quote_plus
from libs.GetSubGachaId import GetGachaSubIdFP

class ParameterBuilder:
    def __init__(self, uid: str, auth_key: str, secret_key: str):
        self.uid_ = uid
        self.auth_key_ = auth_key
        self.secret_key_ = secret_key
        self.content_ = ''
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', str(uuid.uuid4())),
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]

    def AddParameter(self, key: str, value: str):
        self.parameter_list_.append((key, value))

    def Build(self) -> str:
        self.parameter_list_.sort(key=lambda tup: tup[0])
        temp = ''
        for first, second in self.parameter_list_:
            if temp:
                temp += '&'
                self.content_ += '&'
            escaped_key = quote_plus(first)
            if not second:
                temp += first + '='
                self.content_ += escaped_key + '='
            else:
                escaped_value = quote_plus(second)
                temp += first + '=' + second
                self.content_ += escaped_key + '=' + escaped_value

        temp += ':' + self.secret_key_
        self.content_ += '&authCode=' + \
            quote_plus(base64.b64encode(
                hashlib.sha1(temp.encode('utf-8')).digest()))

        return self.content_

    def Clean(self):
        self.content_ = ''
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', str(uuid.uuid4())),
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]


class Rewards:
    def __init__(self, stone, level, ticket):
        self.stone = stone
        self.level = level
        self.ticket = ticket


class Login:
    def __init__(self, name, login_days, total_days, act_max, act_recover_at, now_act, add_fp, total_fp):
        self.name = name
        self.login_days = login_days
        self.total_days = total_days
        self.act_max = act_max
        self.act_recover_at = act_recover_at
        self.now_act = now_act
        self.add_fp = add_fp
        self.total_fp = total_fp


class Bonus:
    def __init__(self, message, items, bonus_name, bonus_detail, bonus_camp_items):
        self.message = message
        self.items = items
        self.bonus_name = bonus_name
        self.bonus_detail = bonus_detail
        self.bonus_camp_items = bonus_camp_items


class user:
    def __init__(self, user_id: str, auth_key: str, secret_key: str):
        self.name_ = ''
        self.user_id_ = (int)(user_id)
        self.s_ = fgourl.NewSession()
        self.builder_ = ParameterBuilder(user_id, auth_key, secret_key)

    def Post(self, url):
        res = fgourl.PostReq(self.s_, url, self.builder_.Build())
        self.builder_.Clean()
        return res

    def topLogin(self):
        DataWebhook = []  # This data will be use in discord webhook!

        lastAccessTime = self.builder_.parameter_list_[5][1]
        userState = (-int(lastAccessTime) >>
                     2) ^ self.user_id_ & fgourl.data_server_folder_crc_

        self.builder_.AddParameter(
            'assetbundleFolder', fgourl.asset_bundle_folder_)
        self.builder_.AddParameter('isTerminalLogin', '1')
        self.builder_.AddParameter('userState', str(userState))

        data = self.Post(
            f'{fgourl.server_addr_}/login/top?_userId={self.user_id_}')

        self.name_ = hashlib.md5(
            data['cache']['replaced']['userGame'][0]['name'].encode('utf-8')).hexdigest()
        stone = data['cache']['replaced']['userGame'][0]['stone']
        lv = data['cache']['replaced']['userGame'][0]['lv']
        ticket = 0

        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 4001:
                ticket = item['num']
                break

        rewards = Rewards(stone, lv, ticket)

        DataWebhook.append(rewards)

        login_days = data['cache']['updated']['userLogin'][0]['seqLoginCount']
        total_days = data['cache']['updated']['userLogin'][0]['totalLoginCount']

        act_max = data['cache']['replaced']['userGame'][0]['actMax']
        act_recover_at = data['cache']['replaced']['userGame'][0]['actRecoverAt']
        now_act = (act_max - (act_recover_at - mytime.GetTimeStamp()) / 300)

        add_fp = data['response'][0]['success']['addFriendPoint']
        total_fp = data['cache']['replaced']['tblUserGame'][0]['friendPoint']

        login = Login(
            self.name_,
            login_days,
            total_days,
            act_max, act_recover_at,
            now_act,
            add_fp,
            total_fp
        )

        DataWebhook.append(login)

        if 'seqLoginBonus' in data['response'][0]['success']:
            bonus_message = data['response'][0]['success']['seqLoginBonus'][0]['message']

            items = []
            items_camp_bonus = []

            for i in data['response'][0]['success']['seqLoginBonus'][0]['items']:
                items.append(f'{i["name"]} x{i["num"]}')

            if 'campaignbonus' in data['response'][0]['success']:
                bonus_name = data['response'][0]['success']['campaignbonus'][0]['name']
                bonus_detail = data['response'][0]['success']['campaignbonus'][0]['detail']

                for i in data['response'][0]['success']['campaignbonus'][0]['items']:
                    items_camp_bonus.append(f'{i["name"]} x{i["num"]}')
            else:
                bonus_name = None
                bonus_detail = None

            bonus = Bonus(bonus_message, items, bonus_name,
                          bonus_detail, items_camp_bonus)
            DataWebhook.append(bonus)
        else:
            DataWebhook.append("No Bonus")

        webhook.topLogin(DataWebhook)

    def drawFP(self):
        self.builder_.AddParameter('storyAdjustIds', '[]')
        self.builder_.AddParameter('gachaId', '1')
        self.builder_.AddParameter('num', '10')
        self.builder_.AddParameter('ticketItemId', '0')
        self.builder_.AddParameter('shopIdIndex', '1')

        if main.fate_region == "NA":
            gachaSubId = GetGachaSubIdFP("NA")
            if gachaSubId is None:
                gachaSubId = "0"  # or any other default value as a string
            self.builder_.AddParameter('gachaSubId', gachaSubId)
            main.logger.info(f"Friend Point Gacha Sub Id " + gachaSubId)
        else:
            gachaSubId = GetGachaSubIdFP("JP")
            if gachaSubId is None:
                gachaSubId = "0"  # or any other default value as a string
            self.builder_.AddParameter('gachaSubId', gachaSubId)
            main.logger.info(f"Friend Point Gacha Sub Id " + gachaSubId)

        data = self.Post(
            f'{fgourl.server_addr_}/gacha/draw?_userId={self.user_id_}')

        responses = data['response']

        servantArray = []
        missionArray = []

        for response in responses:
            resCode = response['resCode']
            resSuccess = response['success']

            if (resCode != "00"):
                continue

            if "gachaInfos" in resSuccess:
                for info in resSuccess['gachaInfos']:
                    servantArray.append(
                        gacha.gachaInfoServant(
                            info['isNew'], info['objectId'], info['sellMana'], info['sellQp']
                        )
                    )

            if "eventMissionAnnounce" in resSuccess:
                for mission in resSuccess["eventMissionAnnounce"]:
                    missionArray.append(
                        gacha.EventMission(
                            mission['message'], mission['progressFrom'], mission['progressTo'], mission['condition']
                        )
                    )

        webhook.drawFP(servantArray, missionArray)

    def topHome(self):
        self.Post(f'{fgourl.server_addr_}/home/top?_userId={self.user_id_}')
