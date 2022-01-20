# HikariWatcher

Introducing automatic hot-reloading of hikari-lightbulb discord bot's plugins! 

Probably a helpful package made for discord bot devs who uses hikari and lightbulb.

This beautiful module watches over your Extensions/Plugins all the time saving you from the pain of re-running the bot again and again while making a small change. 

When your bot is ready to run, just include 
``` 
watch = Watcher(bot, path = "path_to_your_extensions")
await watch.start()
```

```
class Watcher(bot: lightbulb.BotApp,
                path: str = "plugins",
                debug: bool = True,
                loop: asyncio.BaseEventLoop = None,
                default_logger: bool = True,
                preload: bool = True,
                restart: bool = True
        ):
```

1.  bot - lightbulb.BotApp instance of your hikari-lightbulb discord bot
2.  path - Path to your extensions. Defaults to 'plugins'
3.  debug - Whether to run the bot only when the Python `__debug__` flag is True. Defaults to True.
4.  loop: Custom event loop. Defaults to the current running event loop.
5.  default_logger - Whether to use default logger or not. (Only default is available right now)
6.  preload - Preloads all the extensions. Defaults to True
7.  restart - If any serious issue arises (like REGEX errors in slash commands, etc), it restarts the bot. Defaults to True. If set to False, any serious issue would stop the execution right away.


Run testRunner.py to get run tests on example plugins.
Also, to run testRunner.py , create a `.env` file and put `BOT_TOKEN=YOUR_BOT_TOKEN`



This Project is still under development, but is stable for most purposes. There are a couple of bugs to fix which I'll be soon listing out under issues.


Right now, the existing problem at hand is that the bot needs to be re-run when creating a new Plugin file or folders. Making new Plugin file without load/unload might need a re-run.


P.S : Inspired by [cogwatch](https://github.com/robertwayne/cogwatch) by Robert Wayne

