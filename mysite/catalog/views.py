from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from catalog.models import DiscordUser, VoiceStatus



def login_view(request):
    num_users = DiscordUser.objects.all().count()

    num_online_users = ((DiscordUser.objects.filter(status="online").count() +
                        DiscordUser.objects.filter(status="idle").count()) +
                        DiscordUser.objects.filter(status="dnd").count())

    def shorter_string():
        total_count_in_voice = VoiceStatus.objects.all()[:10]
        result = ""
        for i in total_count_in_voice:
            raw_str = str(i)
            short_str = raw_str[:15]
            result += short_str + "<br>"
        return result

    short_string = shorter_string()
    context = {
        'num_users': num_users,
        'num_online_users': num_online_users,
        'users_in_voice': short_string
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