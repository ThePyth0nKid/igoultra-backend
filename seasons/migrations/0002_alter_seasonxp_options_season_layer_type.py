# Generated by Django 5.2 on 2025-06-20 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seasons', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasonxp',
            options={'ordering': ['-xp']},
        ),
        migrations.AddField(
            model_name='season',
            name='layer_type',
            field=models.CharField(choices=[('Real-Life', 'Real-Life'), ('Cyber', 'Cyber'), ('Game', 'Game')], default='Real-Life', help_text='Layer, für den diese Season gilt', max_length=20),
        ),
    ]
