"""
Copyright (c) 2023 EvieePy

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import asyncio

import aiohttp
import asyncpg

import core


async def run() -> None:
    async with aiohttp.ClientSession() as session, asyncpg.create_pool(core.config['DATABASE']['dsn']) as pool:
        async with core.Bot(session=session, pool=pool) as bot:
            await bot.start(core.config['TOKENS']['bot'])


try:
    asyncio.run(run())
except KeyboardInterrupt:
    core.logger.warning('Shutting down due to Keyboard Interrupt...')