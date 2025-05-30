# Generated by Django 5.1.1 on 2024-10-07 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0019_rename_username_usermodel__username'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_id', models.CharField(max_length=500)),
                ('file_type', models.IntegerField(choices=[(1, 'ویدیو'), (2, 'عکس')])),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.usermodel')),
            ],
        ),
        migrations.RemoveField(
            model_name='photomodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='VideoModel',
        ),
        migrations.DeleteModel(
            name='PhotoModel',
        ),
    ]
