import hikari
import lightbulb

import asyncio
import logging
import os
import sys
from functools import wraps
from pathlib import Path

from watchgod import Change, awatch


class Watcher : 

        def __init__(self,
                bot: lightbulb.BotApp,
                path: str = "plugins",
                debug: bool = True,
                loop: asyncio.BaseEventLoop = None,
                default_logger: bool = True,
                preload: bool = True,
        ):

            self.bot = bot
            self.path = path
            self.debug = debug
            self.loop = loop
            self.default_logger = default_logger
            self.preload = preload

        @staticmethod
        def get_plugin_name(path : str) -> str:
            path = os.path.normpath(path)
            return path.split(os.sep)[-1:][0][:-3]

        def get_dotted_plugin_path(self, path: str) -> str:
            """Returns the full dotted path that discord.py uses to load cog files."""
            _path = os.path.normpath(path)
            tokens = _path.split(os.sep)
            rtokens = list(reversed(tokens))

            # iterate over the list backwards in order to get the first occurrence in cases where a duplicate
            # name exists in the path (ie. example_proj/example_proj/commands)
            try:
                root_index = rtokens.index(self.path.split("/")[0]) + 1
            except ValueError:
                raise ValueError("Use forward-slash delimiter in your `path` parameter.")

            return ".".join([token for token in tokens[-root_index:-1]])
        
        def dir_exists(self):
            """Predicate method for checking whether the specified dir exists."""
            return Path(Path.cwd() / self.path).exists()

        def validate_dir(self):
            """Method for raising a FileNotFound error when the specified directory does not exist."""
            if self.dir_exists():
                return True
            else:
                raise FileNotFoundError
        
        async def _start(self):

            while self.dir_exists():
                try:
                    async for changes in awatch(Path.cwd() / self.path):
                        self.validate_dir()  # cannot figure out how to validate within awatch; some anomalies but it does work...

                        reverse_ordered_changes = sorted(changes, reverse=True)

                        for change in reverse_ordered_changes:
                            change_type = change[0]
                            change_path = change[1]

                            filename = self.get_plugin_name(change_path)

                            new_dir = self.get_dotted_plugin_path(change_path)
                            cog_dir = f"{new_dir}.{filename.lower()}" if new_dir else f"{self.path}.{filename.lower()}"

                            if change_type == Change.deleted:
                                await self.unload(cog_dir)
                            elif change_type == Change.added:
                                await self.load(cog_dir)
                            elif change_type == Change.modified and change_type != (Change.added or Change.deleted):
                                # await self.reload(cog_dir)
                                await self.unload(cog_dir)
                                await asyncio.sleep(1) ## To avoid any race-condition
                                await self.load(cog_dir)

                except FileNotFoundError:
                    continue

                else:
                    await asyncio.sleep(1)

            else:
                await self.start()


        async def start(self):
                """Checks for a user-specified event loop to start on, otherwise uses current running loop."""
                _check = False
                while not self.dir_exists():
                    if not _check:
                        logging.error(f"The path {Path.cwd() / self.path} does not exist.")
                        _check = True

                else:
                    logging.info(f"Found {Path.cwd() / self.path}!")
                    if self.preload:
                        await self._preload()

                    if self.check_debug():
                        if self.loop is None:
                            self.loop = asyncio.get_event_loop()

                        logging.info(f"Watching for file changes in {Path.cwd() / self.path}...")
                        self.loop.create_task(self._start())


        def check_debug(self):
            """Determines if the watcher should be added to the event loop based on debug flags."""
            return any([(self.debug and __debug__), not self.debug])


        async def load(self, cog_dir: str):
            """Loads a cog file into the client."""
            try:
                self.bot.load_extensions(cog_dir)
                
            except lightbulb.errors.ExtensionAlreadyLoaded:
                logging.info("Reloading in 5 seconds because Extension is Already loaded")
                await self.unload(cog_dir)
                await asyncio.sleep(5)
                await self.load(cog_dir)

            except lightbulb.errors.CommandAlreadyExists as e:
                self.plugin_error(e)
                logging.error("Stopping the Bot due to existing command name in : " + cog_dir)
                self.restart()

            except lightbulb.errors.ExtensionMissingLoad:
                logging.error("The Plugin doesn't have any load function.: " + cog_dir)
                self.restart()
                
            except ValueError as e: ## For REGEX error in which case bot doesn't unload and load again !
                self.plugin_error(e)
                self.restart()

            except Exception as e:
                self.plugin_error(e)

            else:
                logging.info(f"Cog Loaded: {cog_dir}")


        async def unload(self, cog_dir: str):
            try:
                self.bot.unload_extensions(cog_dir)
            except lightbulb.errors.ExtensionNotLoaded:
                logging.error(f"Extension {cog_dir} not loaded. Loading Extension")
                return

            # except lightbulb.errors.Sa
            
            except lightbulb.errors.ExtensionMissingUnload:
                logging.error(f"The Plugin {cog_dir}doesn't have any unload function.")
                self.restart()

            except Exception as e:
                logging.error("UNLOAD ERROR")
                self.plugin_error(e)
                self.restart()

        ## Restarts the bot
        def restart(self):
            logging.info(" Restarting Bot now !! ")
            os.execv(sys.executable, ['python3'] + [sys.argv[0]])

        ## reload_extensions has some bug in the actual file.
        async def reload(self, cog_dir: str):
            try:
                self.bot.reload_extensions(cog_dir)
            except Exception as e:
                self.plugin_error(e)
        
        ## Displays any error in plugin
        @staticmethod
        def plugin_error(e: Exception):
            logging.exception(e)


        async def _preload(self):
            logging.info("Preloading...")
            for cog in {(file.stem, file) for file in Path(Path.cwd() / self.path).rglob("*.py")}:
                if cog[0] == "__init__":
                    continue
                new_dir = self.get_dotted_plugin_path(cog[1])
                await self.load(".".join([new_dir, cog[0]]))



def watch(**kwargs):
    """Instantiates a watcher by hooking into a Bot client methods' `self` attribute."""

    def decorator(function):
        @wraps(function)
        async def wrapper(client):
            cw = Watcher(client, **kwargs)
            await cw.start()
            retval = await function(client)
            return retval

        return wrapper

    return decorator