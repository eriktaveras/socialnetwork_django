# Generated by Django 4.0.4 on 2022-05-08 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_profile_avatar_profile_link_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar.png', null=True, upload_to='profiles'),
        ),
    ]
