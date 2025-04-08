from django.db import models

class DiscordUser(models.Model):
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="offline")


    def __str__(self):
        return self.username



class VoiceStatus(models.Model):
    users_in_voice = models.TextField()
    channel_name = models.CharField(max_length=100)
    total_count = models.BigIntegerField(default=0)
    last_updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.channel_name} - {self.total_count} "
