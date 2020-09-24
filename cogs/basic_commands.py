# Haqua's Basic Functions
# written by GrenadeSpamr

import discord
from discord.ext import commands
import random
import wikipediaapi
import textwrap

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def haqua(self, ctx):
        await ctx.send("Hi, I am a Heuristic Assistant offering Quality User experience or just an Assistant. Haqua!")

    @commands.command(aliases=['yn', 'yesorno'])
    @commands.is_owner()
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
    async def wiki(self, ctx, *, arg):
        wiki = wikipediaapi.Wikipedia('en')
        wiki_page = wiki.page(arg)
        wikiSum = textwrap.shorten(wiki_page.summary, 500)
        embed = discord.Embed(title=wiki_page.title, url=wiki_page.canonicalurl, description=wikiSum)
#        embed.set_thumbnail(url=wiki.images[0])
        embed.set_footer(text='wikipedia.org')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BasicCommands(bot))
