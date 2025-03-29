from django.contrib import admin
from .models import DiscordUser

class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ('username','user_id','join_date')
    fields = ['username','user_id','join_date']
admin.site.register(DiscordUser,DiscordUserAdmin)
