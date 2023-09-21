<img width="100%" style="border: 1px solid black" src="https://i.imgur.com/bre34Xl.png">

# FGO Daily Login
FGO Daily Login is a mod of the repository [FGODailyBonus](https://github.com/hexstr/FGODailyBonus)

It has the following features:
- No Logs
- Automatic VerCode Update
- Change Telegram to Discord Webhook
- Region JP and NA 

# Extract your auth data
You need to extract your authentication data to do this.
It's simple, all you need to do is navigate to the following path and get the following file: 

| Region | Path | File |
| --- | --- | --- | 
| NA | `android/data/com.aniplex.fategrandorder.en/files/data/` | 54cc790bf952ea710ed7e8be08049531 |
| JP | `android/data/com.aniplex.fategrandorder/files/data/` | 54cc790bf952ea710ed7e8be08049531 |

Copy from ZSv to end, should be ZSv/WkOGiQ25eqY+A5Lgln3pq91NidrEBM/BezdP0gbYJFS6y...

# Discord Webhook 
To create webhook discord you need create a server in discord and create a text channel, in settings of that channel search
`integration > webhook > create webhook > copy url webhook`

# Cron / Scheluded
I configure cron of this repository with [VerCode Extractor Repository](https://github.com/O-Isaac/FGO-VerCode-extractor)
you should configure all cron after update of VerCode Extractor Repository!

| Region | Update VerCode Extractor Repository     | Login in FGO Daily Repository       |
|--------|-------------|-------------|
| NA     | 15 10 * * * | 30 10 * * * |
| JP     | 15 19 * * * | 30 19 * * * |

Is not necesary fork the repo of verCode but if you want
you must change endpoint in main.py in the function `get_latest_verCode`

# Secrets
Add this enviroment variables into `Repository > settings > secrets > actions`
| Secret | Example |
| --- | --- |
| GAME_CERT | ZSv/WkOGiQ25eqY+A5Lgln3pq91NidrEBM/BezdP0gbYJFS6y...,ZSv/WkOGiQ25eqY+A5Lgln3pq91NidrEBM/BezdP0gbYJFS6y... |
| DISCORD_WEBHOOK | https://discord.com/api/webhooks/randomNumber/randomString |

# Road Map
- [x] Perform Daily Friend Point Summons
- [ ] Claim all Saint Quartz and Tickets from gif box 
- [ ] Make blue apple automatic

# Acknowledgments 
- [hexstr](https://github.com/hexstr) author of FGO Daily Bonus
