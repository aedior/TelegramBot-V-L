# Generated by Django 5.1.1 on 2024-10-05 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0013_alter_videomodel_video_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='placeInBot',
            field=models.IntegerField(choices=[(0, 'بدون مکان'), (1, 'افزودن ادمین'), (2, 'افزودن چنل'), (3, 'دلت چنل'), (4, 'پیام همگانی'), (5, 'حذف ادمین')], default=0),
        ),
    ]
