# Haqua's Basic Commands

import discord
import random
import wikipediaapi
import textwrap
from discord.ext import commands
from textwrap import shorten

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.command()
    async def haqua(self, ctx):
        await ctx.send("Hi, I am a Heuristic Assistant offering Quality User experience or just an Assistant. Haqua!")

    @commands.command(aliases=['yn', 'yesorno'])
    async def yesno(self, ctx):
        binary = random.randint(0, 1)
        if binary == 0:
            print(f'Random output: {binary}')
            await ctx.send('Yes')
        else:
            print(f'Random output: {binary}')
            await ctx.send('No')

    @commands.command(aliases=['mcs', 'conchshell'])
    async def magicconchshell(self, ctx):
        answers = [
            "Maybe someday.", "Nothing.", "Neither.",
            "I don't think so.", "No.", "Yes.",
            "Try asking again."
            ]
        await ctx.send(random.choice(answers), tts=False)

    @commands.command()
    async def wiki(self, ctx, *, article):
        wiki = wikipediaapi.Wikipedia('en')
        try:
            wiki_page = wiki.page(article)
            wikiTitle = wiki_page.title
            wikiSum = shorten(wiki_page.summary, 500)
            print(article != wiki_page.title)
            if article != wiki_page.title:
                wikiTitle = '[Redirected] ' + wiki_page.title
                wikiSum = '**Nearest possible result given as the requested article was not available**.\n' + wikiSum
                print("Requested page is not available.")
            embed = discord.Embed(title=wikiTitle, url=wiki_page.fullurl, description=wikiSum)
            embed.set_footer(text='Wikipedia, the free encyclopedia')
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send("The requested article was unavailable. Clarify your query.")
            
def setup(bot):
    bot.add_cog(BasicCommands(bot))
