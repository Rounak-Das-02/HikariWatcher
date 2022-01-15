import hikari
import lightbulb

info_plugin = lightbulb.Plugin("Info3")


@info_plugin.command
@lightbulb.command("hel", "Nothing")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def hel(ctx: lightbulb.Context) -> None:
    await ctx.respond("hel")

@info_plugin.command
@lightbulb.command("hell", "Yo")
@lightbulb.implements(lightbulb.PrefixCommand)
async def hell(ctx : lightbulb.Context) -> None:
    await ctx.respond("hell")

@info_plugin.command
@lightbulb.command("yo" , "YO")
@lightbulb.implements(lightbulb.PrefixCommand)
async def yoo(ctx : lightbulb.Context) -> None:
    await ctx.respond("yo")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(info_plugin)