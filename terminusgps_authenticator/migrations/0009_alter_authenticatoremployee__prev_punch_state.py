# Generated by Django 5.1.7 on 2025-03-10 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminusgps_authenticator', '0008_alter_authenticatoremployeeshift_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticatoremployee',
            name='_prev_punch_state',
            field=models.BooleanField(default=False),
        ),
    ]
