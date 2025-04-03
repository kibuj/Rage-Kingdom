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
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@sync_to_async
def create_or_get_user(user_id, defaults):
    return DiscordUser.objects.get_or_create(user_id=user_id, defaults=defaults)

@sync_to_async
def update_user_status(user_id, status):
    user = DiscordUser.objects.filter(user_id=user_id).first()
    if user:
        user.status = status
        user.save()

@bot.event
async def on_ready():
    print(f'✅✅✅ Бот {bot.user} готовий до роботи ✅✅✅')
    await fetch_members()

async def fetch_members():
    for guild in bot.guilds:
        for member in guild.members:
            defaults = {
                'username': member.name,
                'user_id': str(member.id),
            }
            discord_user, created = await create_or_get_user(member.id, defaults)

            status = str(member.status)
            await update_user_status(member.id, status)  # Перевіряємо статусу

            if created:
                print(f'➕ Added new user: {discord_user.username} (Status: {status})')
            else:
                print(f'👤 User {discord_user.username} already exists. Status: {status}')

#Оновлення статусу
@bot.event
async def on_presence_update(before, after):
    if before.status != after.status:
        new_status = str(after.status)
        await update_user_status(after.id, new_status)
        print(f'🔄 {after.name} змінив статус на {new_status}')


#Додавання нового користувача при  вході на сервер
@bot.event
async def on_member_join(member):
    defaults = {
        'username': member.name,
        'user_id': str(member.id),
    }
    discord_user, created = await create_or_get_user(member.id, defaults)

    if created:
        print(f'🆕 Added new member: {discord_user.username} (Status: {member.status})')
    await update_user_status(member.id, str(member.status))

#Вихід з сервера
@bot.event
async def on_member_remove(member):
    print(f'❌ Вафля ливнула: {member.name}')

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
bot.run(TOKEN)
