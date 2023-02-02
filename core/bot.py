"""
Copyright (c) 2023 EvieePy

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import logging
import tomllib

import aiohttp
import discord
from discord.ext import commands

from .logs import Handler


with open('config.toml', 'rb') as fp:
    config = tomllib.load(fp)


logger: logging.Logger = logging.getLogger(__name__)


# noinspection PyUnresolvedReferences,PyDunderSlots
class Bot(commands.Bot):

    def __init__(self, *, session: aiohttp.ClientSession) -> None:
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        self.session = session

        super().__init__(intents=intents, command_prefix=['p! ', 'p!'])
        discord.utils.setup_logging(handler=Handler(level=config['LOGGING']['level']))

    async def setup_hook(self) -> None:
        pass

    async def on_ready(self) -> None:
        logger.info(f'Logged in as: {self.user} (ID: {self.user.id})')
