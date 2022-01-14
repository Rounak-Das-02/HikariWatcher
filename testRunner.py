import os

import dotenv
import hikari
import lightbulb

from hikariWatcher import Watcher
dotenv.load_dotenv()

bot = lightbulb.BotApp(
    os.environ["BOT_TOKEN"],
    prefix="sudo ",
    banner=None,
    intents=hikari.Intents.ALL,
)


@bot.command
@lightbulb.command("ping", description="The bot's ping")
@lightbulb.implements(lightbulb.PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Latency: {bot.heartbeat_latency*1000:.2f}ms")

@bot.listen(hikari.StartedEvent)
async def on_starting(_: hikari.StartedEvent) -> None:
    # bot.load_extensions("examples.plugin1")
    print("Bot has started ....")
    watch = Watcher(bot, path = "examples", preload=True)
    await watch.start()

if __name__ == "__main__":
    # bot.load_extensions("examples.plugin1")
    # bot.load_extensions_from("./examples/", must_exist=True)
    bot.run()