import discord
from discord.ext import commands
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django


django.setup()

from catalog.models import DiscordUser

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_member_join(member):
    user, created = DiscordUser.objects.get_or_create(
        user_id=member.id,
        defaults={
            'username': member.name,
            'user_id': str(member.id),
        }
    )
    if created:
        print(f'Added new member: {member.name}')

@bot.event
async def on_member_remove(member):
    print(f'Member left: {member.name}')

TOKEN = os.environ['DISCORD_BOT_TOKEN']
bot.run(TOKEN)
