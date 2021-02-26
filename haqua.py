# Haqua's Discord Script
# written by GrenadeSpamr

import discord
import json
import logging
import signal
from discord.ext import commands
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from os import listdir, environ, path

log_file = "logs/haqua.log"
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1000*4096, mode='w', backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
if path.isfile(log_file):
    logger.debug("Log end.")
    handler.doRollover()

load_dotenv()
discord_token = environ.get('discord_token')
game = discord.Game("with GrenadeSpamr")
owner_id = environ.get('owner_id')
bot_id = environ.get('bot_id')

intents = discord.Intents()
intents.messages = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=game)
    await bot.wait_until_ready()
    await bot.application_info()

@bot.event
async def on_message(message):
    format = '[{0.created_at} {0.guild}/{0.channel} - [{0.id}] {0.author}: {0.content}'.format(message)
    print(format)

    if bot.user in message.mentions:
        if str(message.author.id) == owner_id:
            await message.channel.send("Hey :3")
        else:
            await message.delete()
#           await message.channel.send("Please do not mention me.")
#           await message.channel.send(f'{message.author.id} --- {owner_id}')
    await bot.process_commands(message)

@bot.event
async def on_member_update(before, after):
    if str(before.id) == bot_id:
        if after.nick != 'Haqua':
            await after.guild.me.edit(nick='Haqua')
#    else:
#        print(f'User {before.nick} {after.activity}')

@bot.command()
@commands.is_owner()
async def load(ctx, *, cog):
    extensions = cog.split()
    for extension in extensions:
        try:
            bot.load_extension(extension)
            await ctx.send(f"Loaded {extension}")
        except Exception as error:
            await ctx.send(f"Error loading {extension}\n> {error}")

@bot.command()
@commands.is_owner()
async def unload(ctx, *, cog):
    extensions = cog.split()
    for extension in extensions:
        try:
            bot.unload_extension(extension)
            await ctx.send(f"Unloaded {extension}")
        except Exception as error:
            await ctx.send(f"Error unloading {extension}\n> {error}")

@bot.command()
@commands.is_owner()
async def reload(ctx, cog):
    extensions = cog.split()
    for extension in extensions:
        try:
            bot.reload_extension(cog)
            await ctx.send(f"Reloaded extension {cog}")
        except Exception as error:
            await ctx.send(f"Error reloading {extension}\n> {error}")

@bot.command()
@commands.is_owner()
async def listguilds(ctx):
    guilds = []
    for guild in bot.guilds:
        guilds.append(guild.name)
    embed = discord.Embed(title="Connected guilds", description=f'{*guilds,}')
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def logoff(ctx):
    await ctx.send("Log off signal received. Have a good day.")
    await bot.close()

if __name__ == '__main__':
    with open('config/cogs.json') as cogs_json:
        starting_cogs = json.load(cogs_json)['starting_cogs']

    print(f'Discord.py {discord.__version__}')
    for extension in starting_cogs:
        try:
            bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as error:
            print(f"Error loading {extension} ... {error}")
    try:
        bot.run(discord_token)
    except KeyboardInterrupt:
        bot.close()
