import os
from discord.ext import commands
from utils import create_vc, get_category_by_name, get_channel_by_name

CATEGORY = os.getenv("CATEGORY_NAME")
VC_NAME = os.getenv("VC_NAME")

class Activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        
        if not before.channel:
            print(f'{member.name} joined {after.channel.name}')

        if before.channel and not after.channel:
            print(f'User left channel')

        if before.channel and after.channel:
            if before.channel.id != after.channel.id:
                print('User switched VCs')
            else:
                print('Unknown activity')
                if member.voice.self_stream:
                    print(f'{member.name} started streaming')
                elif member.voice.self_mute:
                    print(f'{member.name} muted')
                elif member.voice.self_deaf:
                    print(f'{member.name} deafened')
            
        if after.channel is not None:
            if after.channel.name == VC_NAME:
                existing_channel_name = f"{member.name}'s room".lower()
                existing_channel = get_channel_by_name(after.channel.guild, existing_channel_name)

                if existing_channel is None:
                    print(f"Creating VC for {member.name}")
                    channel = await create_vc(after.channel.guild, existing_channel_name, category_name=CATEGORY)

                    if channel is not None:
                        await member.move_to(channel)
                    else:
                        print("Failed to create voice channel.")
                else:
                    print("Channel already exists. Moving user.")
                    await member.move_to(existing_channel)
        
        if before.channel is not None:
            if before.channel.category.id == get_category_by_name(before.channel.guild, CATEGORY).id:
                print("User left temp channel")
                if len(before.channel.members) == 0:
                    print("channel is empty, deleting")
                    await before.channel.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(Activities(bot))