from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def login_view(request):
    return render(request, 'login.html')

@login_required
def profile(request):
    user = request.user
    discord_login = user.social_auth.get(provider="discord")

    return JsonResponse({
        "username": user.username,
        "discord_id": discord_login.uid,
        "avatar": discord_login.extra_data.get('avatar', ''),
    })