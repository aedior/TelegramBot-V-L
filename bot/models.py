from django.db import models



class PlaceInBot(models.IntegerChoices):
    NONE = 0, "بدون مکان"
    ADD_ADMIN = 1, "افزودن ادمین"
    ADD_CHANNEL = 2, "افزودن چنل"
    DELET_CHANNEL = 3, "دلت چنل"
    ALL_MESSAGE = 4, "پیام همگانی"
    

class UserModel(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    telegram_user_num = models.IntegerField()
    placeInBot = models.IntegerField(choices=PlaceInBot.choices, default=PlaceInBot.NONE)
    chat_id = models.IntegerField()
    first_start = models.DateTimeField(auto_now=True)
    is_join = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    can_add_admin = models.BooleanField(default=False)

class ChannelModel(models.Model):
    _channel_username = models.CharField(max_length=100)
    
    @property
    def channel_username(self):
        return f"@{self._channel_username}"
    
class VideoModel(models.Model):
    user_id = models.IntegerField()
    user_username = models.CharField(max_length=100)
    video_id = models.CharField(max_length=500)