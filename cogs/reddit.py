# Haqua's Reddit Function

import aiohttp
import asyncio
import discord
from PIL import Image
import json
from bs4 import BeautifulSoup
from discord.ext import commands
from textwrap import shorten

class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    # @commands.is_owner()
    async def reddit(self, ctx, source=None, start=1, end=9):
        try:
            with open('config/reddit.json') as rss_json:
                if source:
                    rss_reddit = json.loads(f'{{"subreddit_feed": ["https://reddit.com/r/{source}.rss"]}}')
                else:
                    rss_reddit = json.load(rss_json)
                for feed in rss_reddit["subreddit_feed"]: 
                    async with aiohttp.ClientSession() as session:
                        async with session.get(feed) as resp:
                            file_size = resp.headers['content-length']
                            message = await ctx.send(f"Downloading data... [Bytes: {file_size}]")
                            rss_page = await resp.text()
                    rss_soup = BeautifulSoup(rss_page, 'lxml')
                    rss_scrape = rss_soup.find_all('entry')
                    rss_title =  rss_soup.title.text
                    rss_items = []
                    embed = discord.Embed(title=f'{rss_title}')
                    thumbnails = []
                    
                    for item in rss_scrape[start:end]:
                        rss_item = {}
                        rss_item['title'] = item.title.text
                        rss_item['author'] = item.author.find('name').text
                        rss_item['link'] = item.link['href']
                        content_soup = BeautifulSoup(item.content.text, 'html.parser')

                        if content_soup.find('div'):
                            rss_item['text'] = shorten(content_soup.find('div', class_='md').text, 250)
                        else:
                            rss_item['text'] = ''
                        if content_soup('img'):
                            thumbnails.append(content_soup.find('img')['src'])
                        
                        rss_items.append(rss_item)
                    for item in rss_items:
                        embed.add_field(name='\u200b', value=f"**[{item['title']}]({item['link']})\n {item['author']}**\n {item['text']}", inline=False)
                        embed.set_footer(text=rss_title)
                    
                    async def fetch(item, session):
                        async with session.get(item) as resp:
                            return await resp.read()
                    
                    queue = []
                    async with aiohttp.ClientSession() as session:
                        for item in thumbnails:
                            job = asyncio.ensure_future(fetch(item, session))
                            queue.append(job) 
                        thumbnail_data = await asyncio.gather(*queue)
                        
                    for index, item in enumerate(thumbnail_data):
                        open(f'cache/thumbnail{index}.png', 'wb').write(item)

                    async def thumbnail_collage(width, height, thumbnail_data):           
                        collage = Image.new('RGB', (width, height))
                        image_list = []
                        
                        for index, image in enumerate(thumbnail_data):
                            image_size = 100, 100
                            piece = Image.open(f'cache/thumbnail{index}.png')
                            image_list.append(piece.resize((100, 100)))
                            
                        while len(image_list) < 6:
                            piece = Image.new('RGB', (100, 100))
                            image_list.append(piece)

                        i = 0
                        for x in range(0, 300, 100):
                            for y in range(0, 200, 100):
                                # await ctx.send(f'{i, x, y}')
                                collage.paste(image_list[i], (x, y))
                                i += 1
                                y += 30
                        collage.save('cache/collage.png')
                        
                    if content_soup('img'):
                        await thumbnail_collage(300, 200, thumbnail_data)
                        file = discord.File('cache/collage.png')
                        embed.set_image(url='attachment://collage.png')
                        await ctx.send(embed=embed, file=file)
                    else:
                        await ctx.send(embed=embed)
                    await message.delete()
            
        except Exception as error:
            await ctx.send("An error has occurred.")
            raise Exception
            
    # @commands.command()
    # @commands.has_permissions(manage_messages=True)
    # async def subscribe(self, ctx, time):
    

def setup(bot):
    bot.add_cog(Reddit(bot))
