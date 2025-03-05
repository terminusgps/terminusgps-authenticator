# Generated by Django 5.1.6 on 2025-03-05 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminusgps_authenticator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authenticatoremployee',
            name='pfp',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='', verbose_name='profile picture'),
        ),
        migrations.AddField(
            model_name='authenticatoremployee',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]
