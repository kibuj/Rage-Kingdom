# Generated by Django 5.1.7 on 2025-04-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_discorduser_join_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='discorduser',
            name='status',
            field=models.CharField(default='offline', max_length=20),
        ),
    ]
