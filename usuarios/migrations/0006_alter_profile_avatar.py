# Generated by Django 4.0.4 on 2022-05-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar.jpg', null=True, upload_to='profiles'),
        ),
    ]
