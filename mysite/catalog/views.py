from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from catalog.models import DiscordUser


def login_view(request):
    num_users = DiscordUser.objects.all().count()

    num_online_users = ((DiscordUser.objects.filter(status="online").count() +
                        DiscordUser.objects.filter(status="idle").count()) +
                        DiscordUser.objects.filter(status="dnd").count())

    context = {
        'num_users': num_users,
        'num_online_users': num_online_users,
    }

    return render(request, 'index.html', context=context)

@login_required
def profile(request):
    user = request.user
    discord_login = user.social_auth.get(provider="discord")

    return JsonResponse({
        "username": user.username,
        "discord_id": discord_login.uid,
        "avatar": discord_login.extra_data.get('avatar', ''),
    })