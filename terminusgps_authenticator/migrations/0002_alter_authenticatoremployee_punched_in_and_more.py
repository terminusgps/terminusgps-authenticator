# Generated by Django 5.1.6 on 2025-02-28 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminusgps_authenticator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticatoremployee',
            name='punched_in',
            field=models.BooleanField(db_column='punched_in', default=False),
        ),
        migrations.RenameField(
            model_name='authenticatoremployee',
            old_name='punched_in',
            new_name='_punched_in',
        ),
    ]
