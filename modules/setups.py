"""
Copyright (c) 2023 EvieePy

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import asyncpg
import discord
from discord.ext import commands

import core


class Setups(commands.Cog):

    def __init__(self, bot: core.Bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.hybrid_group()
    async def setup(self, ctx: commands.Context) -> None:
        pass

    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @setup.command()
    async def autorooms(self, ctx: commands.Context) -> None:
        """Setup Auto Voice Rooms for your server."""

        async with self.bot.pool.acquire() as connection:
            query: str = """SELECT cid FROM rooms WHERE gid = $1"""
            result: asyncpg.Record = await connection.fetchrow(query, ctx.guild.id)

        if result:
            channel: discord.CategoryChannel = self.bot.get_channel(int(result['cid']))
            await ctx.send(f'AutoRooms have already been setup in this server. See: {channel.mention}', ephemeral=True)

            return

        category: discord.CategoryChannel = await ctx.guild.create_category_channel(name='Auto Rooms')
        channel: discord.VoiceChannel = await category.create_voice_channel(name='Create a Room \U0001F4E2')

        rooms_cog: commands.Cog = self.bot.get_cog('AutoRooms')
        rooms_cog.rooms[category.id] = channel.id

        async with self.bot.pool.acquire() as connection:
            query: str = """INSERT INTO rooms(gid, cid, vid) VALUES($1, $2, $3)"""
            await connection.execute(query, ctx.guild.id, category.id, channel.id)

        await ctx.send(f'Successfully setup AutoRooms for this server. See: {category.mention}', ephemeral=True)


async def setup(bot: core.Bot) -> None:
    await bot.add_cog(Setups(bot))
