import discord
import sys
import os
from asgiref.sync import sync_to_async


sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

from catalog.models import DiscordUser

@sync_to_async
def create_or_get_user(user_id, defaults):
    return DiscordUser.objects.get_or_create(user_id=user_id, defaults=defaults)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await fetch_members()

async def fetch_members():
    for guild in bot.guilds:
        async for member in guild.fetch_members(limit=None):
            user_id = member.id
            defaults = {
                'username': member.name,
                'user_id': str(member.id),
            }
            discord_user, created = await create_or_get_user(user_id, defaults)

            if created:
                print(f'Added new user: {discord_user.username}')
            else:
                print(f'User {discord_user.username} already exists.')

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
bot.run(TOKEN)
