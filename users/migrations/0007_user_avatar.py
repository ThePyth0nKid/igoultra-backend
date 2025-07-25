# Generated by Django 5.2 on 2025-07-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Optional: Hochgeladenes Avatar-Bild (PNG/JPG)', null=True, upload_to='avatars/'),
        ),
    ]
