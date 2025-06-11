import discord
reaction_role_messages = {}

async def create_reaction_message_function(bot, message_id: int, emoji_role_map: dict):
    reaction_role_messages[message_id] = emoji_role_map

    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                message = await channel.fetch_message(message_id)
                for emoji in emoji_role_map:
                    await message.add_reaction(emoji)
                return
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                continue
