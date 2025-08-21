from mcstatus import JavaServer
from dotenv import load_dotenv
from discord.ext import commands
import logging
import discord
import math
import os

# Loading intents, bot token & establishing logger
load_dotenv('.env')
BOT_TOKEN = os.getenv('DC')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    global guild
    for guild in bot.guilds:
        if guild.name == guild:
            break

    # Bot connection info
    logger.info(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    # Commands sync
    try:
        logger.info("Synced commands: \n")
        synced = await bot.tree.sync()
        for x in synced:
            logger.info(f'{x}\n')
        if synced is None:
            logger.info(f'{x} is not synced\n')

    except Exception as error:
        logger.info(error)

def getServerData():
    # Server Lookup
    try:
        server_ip = 'kirahosting.fun:25565'
        server = JavaServer.lookup(server_ip)
    except Exception:
        logger.error('There has been an error while trying to look up the server ...')
        return 'Error'

    # Server query
    try:
        query = server.query()
        playerlist = query.players.list
        latency = server.ping()
    except Exception:
        logger.error('There haas been an error with query-ing the server for data ...')
        return 'Error'

    return [playerlist, latency]

@bot.tree.command(name='server-status', description='Get current server status with playerlist and latency')
async def getStatus(interaction: discord.Interaction):
    data = getServerData()
    if data == 'Error':
        await interaction.response.send_message('There has been an error with extracting servers data ...', ephemeral=True)
    
    playerlist = ', '.join(data[0])
    latency = math.ceil(data[1])

    await interaction.response.send_message(f'Server is online ! Player list: {playerlist}; Ping response time is ~{latency}ms')

def main():
    bot.run(BOT_TOKEN)

if __name__ == '__main__':
    main()