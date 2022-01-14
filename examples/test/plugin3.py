import hikari
import lightbulb

info_plugin = lightbulb.Plugin("Info")


@info_plugin.command
@lightbulb.command(
    "hello", "Nothing"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def hello(ctx: lightbulb.Context) -> None:
    await ctx.respond("hello")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(info_plugin)