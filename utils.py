def get_category_by_name(guild, category_name):
    category = None
    for c in guild.categories:
        if c.name == category_name:
            category = c
            break
    return category
    
def get_channel_by_name(guild, channel_name):
    channel = None
    for c in guild.channels:
        if c.name == channel_name:
            channel = c
            break
    return channel

async def create_vc(guild, channel_name, category_name, user_limit=None):
    """
    Creates a new channel in the specified category
    """
    category = get_category_by_name(guild, category_name)
    await guild.create_voice_channel(channel_name, category=category, user_limit=user_limit)
    channel = get_channel_by_name(guild, channel_name)
    return channel