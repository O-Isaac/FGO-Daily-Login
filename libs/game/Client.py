import libs.models.user as User
import libs.network.fgourl as Network
import libs.utils.logs as Logger

import time

def Login(userId: str, authKey: str, secretKey: str, region: str):
    Logger.info("Setting latest assets")
    Network.set_latest_assets(region)
    time.sleep(2)

    try:
        client = User.Client(userId, authKey, secretKey)
        
        Logger.info("Logging in...")
        client.topLogin(region)
        time.sleep(2)

        Logger.info("Drawing friend point gacha")
        client.drawFP(region)
        time.sleep(2)
        
        Logger.info("Logging out...")
        client.topHome()        
    except Exception as ex:
        Logger.error(ex)