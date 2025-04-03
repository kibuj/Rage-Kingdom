import discord
from discord.ext import commands
import sys
import os
from asgiref.sync import sync_to_async

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from catalog.models import DiscordUser

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@sync_to_async
def create_or_get_user(user_id, defaults):
    return DiscordUser.objects.get_or_create(user_id=user_id, defaults=defaults)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await fetch_members()

async def fetch_members():
    for guild in bot.guilds:
        async for member in guild.fetch_members(limit=None):
            defaults = {
                'username': member.name,
                'user_id': str(member.id),
            }
            discord_user, created = await create_or_get_user(member.id, defaults)

            if created:
                print(f'Added new user: {discord_user.username}')
            else:
                print(f'User {discord_user.username} already exists.')

@bot.event
async def on_member_join(member):
    defaults = {
        'username': member.name,
        'user_id': str(member.id),
    }
    discord_user, created = await create_or_get_user(member.id, defaults)

    if created:
        print(f'Added new member: {discord_user.username}')

@bot.event
async def on_member_remove(member):
    print(f'Member left: {member.name}')

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
bot.run(TOKEN)
