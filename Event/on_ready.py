import discord

from Misc.create_reaction_message import create_reaction_message_function

async def on_ready_event(bot):
    print(f"Bot ist eingeloggt als {bot.user}")
    await create_reaction_message_function(bot, 1383000886543908876, {
        "💻": 1364631941307043972, # PC
        "🎮": 1364631972621844541, # Playstation
        "🟢": 1364632015042908180, # XBox
        "🔴": 1364632054335144056# Switch
    })
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='!help')
    )
