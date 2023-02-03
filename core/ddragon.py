"""
Copyright (c) 2023 EvieePy

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from __future__ import annotations

import asyncio
import io
import pathlib
import shutil
import tarfile
import typing

import asyncpg
from discord.ext import tasks

if typing.TYPE_CHECKING:
    from .bot import Bot, logger


VERSIONS: str = 'https://ddragon.leagueoflegends.com/api/versions.json'
DOWNLOAD: str = 'https://ddragon.leagueoflegends.com/cdn/dragontail-{version}.tgz'


class DDragon:

    def __init__(self, *, bot: Bot, log: logger) -> None:
        self.bot = bot
        self.logger = log
        self.last: str | None = None

        self.update_loop.start()

    @tasks.loop(hours=6)
    async def update_loop(self) -> None:

        if not self.last:
            async with self.bot.pool.acquire() as connection:
                query: str = """SELECT * FROM ddragon"""
                results: list[asyncpg.Record] = await connection.fetchrow(query)

                if results:
                    self.last = results[0]['version']

        async with self.bot.session.get(url=VERSIONS) as resp:
            latest: str = (await resp.json())[0]

        if latest != self.last:
            asyncio.create_task(self.update(version=latest))

    async def update(self, *, version: str) -> None:
        pass
