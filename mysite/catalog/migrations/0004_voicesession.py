# Generated by Django 5.1.7 on 2025-04-06 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_discorduser_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.BigIntegerField()),
                ('channel_name', models.CharField(max_length=100)),
                ('joined_at', models.DateTimeField()),
                ('left_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.discorduser')),
            ],
        ),
    ]
