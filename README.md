# ItsMingo

This bot allowed you to set up reaction roles to (un)assign roles.
In addition, a bot trap is possible by using the same command (use the bot role as bait) and then add the :skull: emoji!

## Setup

You need to set up an .env file with the following content:
```
DISCORD_BOT_TOKEN=""
GUILD_ID=""

FILENAME_REACTION_ROLES=""
FILENAME_LOG_CONFIG=""
```

* **DISCORD_BOT_TOKEN** - Your Bot Token
* **GUILD_ID** - The server you want the bot to work in
* **FILENAME_REACTION_ROLES** - The Filename (same hierarchy) of the Reaction Roles .json file (e.g., reaction_roles.json)
* **FILENAME_LOG_CONFIG** - The Filename (same hierarchy) of the Bot Log Channel (e.g., bot_log_channelid.json)