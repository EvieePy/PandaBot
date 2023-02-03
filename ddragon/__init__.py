"""
Copyright (c) 2023 EvieePy

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import pathlib

from discord.ext import tasks

import core


VERSIONS: str = 'https://ddragon.leagueoflegends.com/api/versions.json'
DOWNLOAD: str = 'https://ddragon.leagueoflegends.com/cdn/dragontail-{version}.tgz'


class DDragon:

    def __init__(self, bot: core.Bot) -> None:
        self.bot = bot
        self.last: str | None = None
