# ItsMingo

This bot allowed you to set up reaction roles to (un)assign roles.

In addition, a bot trap is possible by using the same command (use the bot role as bait) and then add the :skull: emoji!

Furthermore, it logs when a user reacts to an emoji for the role (un)assignment, as well as logging when a user joined & left the server, and also when someone triggered the bot trap.

## Requirements Installation

To install the necessary Python packages, you need Python 3.12 & execute the following pip command for it:
```
pip install -r requirements.txt
```

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

## Commands

* **/mingo create_reaction channelmsg role1 emoji1 [optional 2-5 roles and emojis]** - Create a Channel Message the command is being used in to add Roles + Reaction Emoji
* **/mingo setlogchannel #ChannelName** - Set the bot to a channel to redirect the log messages