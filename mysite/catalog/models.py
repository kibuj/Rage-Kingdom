from django.db import models

class DiscordUser(models.Model):
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="offline")


    def __str__(self):
        return self.username



class VoiceSession(models.Model):
    user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)
    channel_id = models.BigIntegerField()
    channel_name = models.CharField(max_length=100)
    joined_at = models.DateTimeField()
    left_at = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return f"{self.user.username} in {self.channel_name} "
