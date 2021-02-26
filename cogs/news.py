# Haqua's News RSS Function

import aiohttp
import discord
import json
from bs4 import BeautifulSoup
from discord.ext import commands

class News(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.is_owner()
    async def news(self, ctx, source_limit=2, article_limit=4):
        with open('config/news.json') as rss_json:
            rss_news = json.load(rss_json)
            for feed in rss_news['news_feeds']:
                user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
                async with aiohttp.ClientSession(headers=user_agent) as session:
                    async with session.get(feed) as resp:
                        # file_size = resp.headers['content-length']
                        # message = await ctx.send(f"Downloading data... [Bytes: {file_size}]")
                        rss_page = await resp.text()
                        # await ctx.send(rss_page[:1500])
                        rss_soup = BeautifulSoup(rss_page, 'lxml')
                        rss_scrape = rss_soup.find_all('item')
                        rss_title =  rss_soup.title.text
                        rss_items = []
                        embed = discord.Embed(title=rss_title)
                        
                        for item in rss_scrape[:article_limit]:
                            rss_item = {}
                            rss_item['title'] = item.title.text
                            rss_item['description'] = item.description.text
                            rss_item['pubdate'] = item.pubdate.text
                            rss_item['link'] = item.guid.text
                            rss_items.append(rss_item)
                        for item in rss_items:
                            embed.add_field(name='\u200b', value=f"**[{item['title']}]({item['link']})\n {item['pubdate'][:-5]}**\n {item['description']}", inline=False)
                            embed.set_footer(text=rss_title)
                await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(News(bot))
