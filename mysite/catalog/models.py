from django.db import models

class DiscordUser(models.Model):
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="offline")

    def __str__(self):
        return self.username

