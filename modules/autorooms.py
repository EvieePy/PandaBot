"""
Copyright (c) 2023 EvieePy

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import asyncio
import time

import asyncpg
import discord
from discord.ext import commands, tasks

import core


class AutoRooms(commands.Cog):

    def __init__(self, bot: core.Bot) -> None:
        self.bot = bot

        self.rooms: dict[int, int] = {}
        self.created: dict[str, int] = {}
        self.vacant: dict[int, float] = {}

        self.clear_vacant.start()
        asyncio.create_task(self.load_state())

    @tasks.loop(seconds=15)
    async def clear_vacant(self) -> None:

        for channel_id, timestamp in self.vacant.copy().items():
            channel = self.bot.get_channel(channel_id)

            if not channel:
                del self.vacant[channel_id]
                continue

            if timestamp + 300 <= time.time():
                if len(channel.members) > 0:
                    del self.vacant[channel_id]
                    continue

                try:
                    await channel.delete(reason='AutoRoom channel vacant for 5+ minutes.')
                    del self.vacant[channel_id]
                except discord.HTTPException:
                    pass

    @clear_vacant.before_loop
    async def clear_vacant_before(self) -> None:
        await self.bot.wait_until_ready()

    async def load_state(self) -> None:
        await self.bot.wait_until_ready()

        async with self.bot.pool.acquire() as connection:
            query: str = """SELECT * FROM rooms"""

            results: list[asyncpg.Record] = await connection.fetch(query)

        for result in results:
            self.rooms[result['cid']] = result['vid']

            category: discord.CategoryChannel = self.bot.get_channel(result['cid'])

            for vc in category.voice_channels:
                if vc.id == result['vid']:
                    continue

                if len(vc.members) == 0:
                    self.vacant[vc.id] = time.time()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:

        if channel.type is discord.ChannelType.category:
            async with self.bot.pool.acquire() as connection:
                query: str = """SELECT * FROM rooms WHERE cid = $1"""
                result: asyncpg.Record | None = await connection.fetchrow(query, channel.id)

                if not result:
                    return

                query: str = """DELETE FROM rooms WHERE cid = $1"""
                await connection.execute(query, channel.id)

                try:
                    await (self.bot.get_channel(int(result['vid']))).delete(reason='Deleted AutoRooms category.')
                except discord.HTTPException:
                    pass

                del self.rooms[channel.id]

        elif channel.type is discord.ChannelType.voice:
            async with self.bot.pool.acquire() as connection:
                query: str = """SELECT * FROM rooms WHERE vid = $1"""
                result: asyncpg.Record | None = await connection.fetchrow(query, channel.id)

                if not result:
                    return

                query: str = """DELETE FROM rooms WHERE vid = $1"""
                await connection.execute(query, channel.id)

                try:
                    await channel.category.delete(reason='Deleted Create a Room from AutoRooms.')
                except discord.HTTPException:
                    pass

                del self.rooms[channel.category_id]

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
    ) -> None:

        try:
            owned: discord.VoiceChannel | None = self.bot.get_channel(self.created[f'{member.guild.id}{member.id}'])
            if not owned:
                del self.created[f'{member.guild.id}{member.id}']

        except KeyError:
            owned = None

        in_: bool = after.channel and after.channel.id in self.rooms.values()

        if in_ and not owned:
            channel: discord.VoiceChannel = \
                await after.channel.category.create_voice_channel(name=f'{member.display_name}\'s Room')
            self.created[f'{member.guild.id}{member.id}'] = channel.id

            await channel.set_permissions(
                member,
                mute_members=True,
                deafen_members=True,
                manage_channels=True,
                stream=True,
                manage_messages=True
            )

            await member.move_to(channel)
            return

        if in_ and owned:
            await member.move_to(owned)

            try:
                del self.vacant[after.channel.id]
            except KeyError:
                pass

            return

        if before.channel and before.channel.id in self.created.values() and len(before.channel.members) == 0:
            self.vacant[before.channel.id] = time.time()
            return

        if in_:
            try:
                del self.vacant[after.channel.id]
            except KeyError:
                pass


async def setup(bot: core.Bot) -> None:
    await bot.add_cog(AutoRooms(bot))
