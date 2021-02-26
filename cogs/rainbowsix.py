# Haqua's Rainbow Six Siege Stats Lookup Function

import discord
import r6sapi as r6
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from os import environ

class RainbowSix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.auth = r6.Auth(environ.get('ubi_email'), environ.get('ubi_pass'))
        
    @commands.command()
    async def r6stat(self, ctx, username=None, region=None, platform=None):
        self.auth.refresh_session()
        if username == None:
            username = ctx.author.name
        if region == None:
            region = 'ASIA'
        if platform == None:
            platform = 'uplay'
        
        try:
            await self.auth.refresh_session()
            player = await self.auth.get_player(username, r6.Platforms.UPLAY)
            rank = await player.get_rank('ASIA')
            await player.check_general()
            await player.check_level()
            await player.check_queues()
            # operators = await player.get_all_operators()
            
            embed = discord.Embed(title='Player Statistics')
            embed.set_author(name=player.name, url=player.url, icon_url=player.icon_url)
            
            time_played = player.time_played / 3600
            kd_overall = player.kills / player.deaths
            win_overall = (player.matches_won / player.matches_played) * 100
          
            kd_casual = player.casual.kills / player.casual.deaths
            win_casual = (player.casual.won / player.casual.played) * 100
            
            embed.add_field(name='Level', value=player.level, inline=True)
            embed.add_field(name='Hours Played', value=int(time_played), inline=True)
            
            if player.ranked.played > 0:
                embed.add_field(name='Current Rank', value=f"{rank.RANKS[rank.rank_id]} ({int(rank.mmr)})\n\xb1{rank.skill_stdev:.2f}", inline=False)
            embed.add_field(name='Overall Stats', value=f"K/D: {round(kd_overall, 2)}\nWin%: {round(win_overall, 2)}", inline=False)
            
            if player.ranked.played == 0:
                embed.add_field(name='Ranked Stats', value=f"No data", inline=False)
            if player.ranked.played > 0:
                kd_ranked = player.ranked.kills / player.ranked.deaths
                win_ranked = (player.ranked.won / player.ranked.played) * 100
                embed.add_field(name='Ranked Stats', value=f"K/D: {round(kd_ranked, 2)}\nWin%: {round(win_ranked, 2)}", inline=False)
            embed.add_field(name='Casual Stats', value=f"K/D: {round(kd_casual, 2)}\nWin%: {round(win_casual, 2)}", inline=False)
            # embed.add_field(name='K/D', value=round(kd_ratio, 2), inline=True)
            # embed.add_field(name='KOST', value='N/A (Soon)', inline=True)
            # embed.add_field(name='Ranked K/D', value=round(kd_ranked, 2), inline=True)
            # embed.add_field(name='Ranked Win %', value=round(win_percent, 2), inline=True)
            # embed.add_field(name='Kills', value=f'{player.kills}', inline=True)
            # embed.add_field(name='Deaths', value=f'{player.deaths}', inline=True)
            # embed.add_field(name='Assists', value=f'{player.kill_assists}', inline=True)
            # embed.add_field(name='Top Attacker', value=max(operators, key=timeplayed), inline=True)
            embed.set_footer(text="Tom Clancy's Rainbow Six Siege")
            await self.auth.close()
            await ctx.send(embed=embed)
        
        except Exception as error:
            await self.auth.close()
            await ctx.send(f'> ```{error}```An error occured looking up [{username}]')

def setup(bot):
    bot.add_cog(RainbowSix(bot))
