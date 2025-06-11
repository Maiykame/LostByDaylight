import discord

async def sudo_command(ctx, *, message):
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass
    await ctx.send(message)
