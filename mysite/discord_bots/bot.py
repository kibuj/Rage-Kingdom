import discord
from discord.ext import commands
import sys
import os
from asgiref.sync import sync_to_async
import asyncio

sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from catalog.models import DiscordUser, VoiceStatus

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = True
intents.voice_states = True


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

@sync_to_async
def update_voice_stat(total_count_in_voice, member_names, channel_name):
    stats, _ = VoiceStatus.objects.get_or_create(id=1)
    stats.total_count = total_count_in_voice
    stats.users_in_voice = member_names
    stats.channel_name = channel_name
    stats.save()


@bot.event
async def on_ready():
    print(f'✅✅✅ Бот {bot.user} готовий до роботи ✅✅✅')
    await fetch_members()
    bot.loop.create_task(monitor_voice_channels())

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

async def monitor_voice_channels():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("\n🔁 Перевірка голосових каналів:")
        all_members_names = []
        active_channel_name = ''

        for guild in bot.guilds:
            total_count_in_voice = 0
            for channel in guild.voice_channels:
                members = channel.members
                if members:
                    count = len(members)
                    total_count_in_voice += count
                    member_names = ', '.join([member.name for member in members])
                    all_members_names.append(member_names)
                    print(f"🟢 Канал '{channel.name}': {member_names}")
                    active_channel_name = channel.name
                else:
                    pass

            joined_names = ' | '.join(all_members_names)
            print(f'🔢Загалом у voice:{total_count_in_voice}')


        await update_voice_stat(
            total_count_in_voice = total_count_in_voice,
            member_names = joined_names,
            channel_name = active_channel_name)

        await asyncio.sleep(60)




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
