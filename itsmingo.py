# Bot written by MinoFloof
# Code Refactor by ChatGPT

import discord
import os
import time

from discord import app_commands
from dotenv import load_dotenv
from enum import Enum
from reaction_role_manager import load_json_data, save_json_data

# ─────────── Load Config ───────────
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
FILENAME_REACTION_ROLES = os.getenv("FILENAME_REACTION_ROLES")
FILENAME_LOG_CONFIG = os.getenv("FILENAME_LOG_CONFIG")

# ─────────── Intents ───────────
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
server_guild = discord.Object(id=GUILD_ID)

# ─────────── Data ───────────
reaction_role_messages = load_json_data(FILENAME_REACTION_ROLES)
log_config = load_json_data(FILENAME_LOG_CONFIG)

# ─────────── Constants ───────────
TRAP_EMOJI = "💀"
COMMAND_ROOT = "mingo"
mingo_group = app_commands.Group(name=COMMAND_ROOT, description="Utility Commands")


# ─────────── Enums ───────────
class ReactionType(Enum):
    ADD = "add"
    REMOVE = "remove"


# ─────────── Utility Functions ───────────
def get_log_channel():
    log_channel_id = log_config.get("log_channel_id")
    return client.get_channel(log_channel_id) if log_channel_id else None


async def log_event(content: str):
    log_channel = get_log_channel()
    if log_channel:
        timestamp = int(time.time())
        await log_channel.send(f"<t:{timestamp}:f> - {content}")


def build_role_emoji_pairs(*args):
    return [
        (role, emoji) for role, emoji in zip(args[::2], args[1::2]) if role and emoji
    ]


# ─────────── Commands ───────────
@mingo_group.command(
    name="setlogchannel", description="Set the channel for all bot logs"
)
async def set_log_channel(
    interaction: discord.Interaction, channel: discord.TextChannel
):
    if interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message(
            "❌ Only the server owner can do this.", ephemeral=True
        )
        return

    log_config["log_channel_id"] = channel.id
    save_json_data(FILENAME_LOG_CONFIG, log_config)

    await interaction.response.send_message(
        f"✅ Log channel set to {channel.mention}", ephemeral=True
    )


@mingo_group.command(
    name="create_reaction", description="Create a message with Reaction-Role linkage"
)
async def create_reaction_message(
    interaction: discord.Interaction,
    channelmsg: str,
    role1: discord.Role,
    emoji1: str,
    role2: discord.Role = None,
    emoji2: str = None,
    role3: discord.Role = None,
    emoji3: str = None,
    role4: discord.Role = None,
    emoji4: str = None,
    role5: discord.Role = None,
    emoji5: str = None,
):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message(
            "❌ You don't have permission to use this command.", ephemeral=True
        )
        return

    role_emoji_pairs = build_role_emoji_pairs(
        role1, emoji1, role2, emoji2, role3, emoji3, role4, emoji4, role5, emoji5
    )

    bot_top_role = interaction.guild.me.top_role
    for role, _ in role_emoji_pairs:
        if bot_top_role < role:
            await interaction.response.send_message(
                f"❌ I cannot assign the role '{role.name}' because it's above my highest role.",
                ephemeral=True,
            )
            return

    role_info_block = "\n\n" + "\n".join(
        [f"{emoji}: `{role.name}`" for role, emoji in role_emoji_pairs]
    )
    full_message = channelmsg.replace("\\n", "\n") + role_info_block
    message = await interaction.channel.send(full_message)

    message_map = {}
    for role, emoji in role_emoji_pairs:
        try:
            await message.add_reaction(emoji)
            message_map[emoji] = role.id
        except discord.HTTPException:
            await interaction.followup.send(
                f"❌ Failed to add emoji `{emoji}` for role `{role.name}`.",
                ephemeral=True,
            )
            return

    reaction_role_messages[str(message.id)] = message_map
    save_json_data(FILENAME_REACTION_ROLES, reaction_role_messages)

    await interaction.response.send_message(
        "✅ Message sent with role reactions.", ephemeral=True
    )


# ─────────── Reaction Logic ───────────
async def handle_reaction(
    payload: discord.RawReactionActionEvent, reaction_type: ReactionType
):
    message_id = str(payload.message_id)
    emoji = str(payload.emoji)

    role_map = reaction_role_messages.get(message_id)
    if not role_map:
        return

    role_id = role_map.get(emoji)
    if not role_id:
        return

    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = guild.get_role(role_id)

    if not member:
        return

    if emoji == TRAP_EMOJI and reaction_type == ReactionType.ADD:
        await guild.ban(member, reason="Bot Trap triggered!")
        await log_event(
            f"💀 **'{str(member)}'** was **banned** for triggering the trap emoji."
        )
        return

    if not role:
        return

    if reaction_type == ReactionType.ADD:
        await member.add_roles(role, reason="Reaction role assigned.")
        await log_event(f"✅ **'{str(member)}'** was given the role **'{role.name}'**.")
    else:
        await member.remove_roles(role, reason="Reaction role removed.")
        await log_event(f"❌ **'{str(member)}'** removed the role **'{role.name}'**.")


# ─────────── Events ───────────
@client.event
async def on_ready():
    tree.add_command(mingo_group, guild=server_guild)
    await tree.sync(guild=server_guild)
    print("✅ Bot is ready and commands are synced.")


@client.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    await handle_reaction(payload, ReactionType.ADD)


@client.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    await handle_reaction(payload, ReactionType.REMOVE)


@client.event
async def on_member_join(member: discord.Member):
    await log_event(f"📥 **'{str(member)}'** joined the server.")


@client.event
async def on_member_remove(member: discord.Member):
    await log_event(f"📤 **'{str(member)}'** left the server.")


# ─────────── Run the Bot ───────────
client.run(DISCORD_BOT_TOKEN)
