async def kick(ctx, member, reason="Kein Grund angegeben"):
    if not member.kickable:
        return await ctx.send("Ich kann diesen Benutzer nicht kicken.")
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} wurde gekickt. Grund: {reason}")
