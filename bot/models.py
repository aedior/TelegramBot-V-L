from django.db import models



class PlaceInBot(models.IntegerChoices):
    NONE = 0, "بدون مکان"
    ADD_ADMIN = 1, "افزودن ادمین"
    ADD_CHANNEL = 2, "افزودن چنل"
    DELET_CHANNEL = 3, "دلت چنل"
    ALL_MESSAGE = 4, "پیام همگانی"
    DELETE_ADMIN = 5, "حذف ادمین"
    

class UserModel(models.Model):
    _username = models.CharField(default="none", max_length=100, null=True, blank=True)
    placeInBot = models.IntegerField(choices=PlaceInBot.choices, default=PlaceInBot.NONE)
    chat_id = models.IntegerField()
    first_start = models.DateTimeField(auto_now=True)
    is_join = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    can_add_admin = models.BooleanField(default=False)
    postId = models.IntegerField(default=0)

    @property
    def username(self):
        if self._username is not None:
            return f"@{self._username}"
        else:
            return "بدون نام کاربری"
    
    
class ChannelModel(models.Model):
    _channel_username = models.CharField(max_length=100)
    users = models.IntegerField()
    
    
    @property
    def channel_username(self):
        return f"@{self._channel_username}"



class FileType(models.IntegerChoices):
    VIDEO = 1, "ویدیو"
    PHOTO = 2, "عکس"


class FileModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    hash_id = models.CharField(max_length=500)
    file_type = models.IntegerField(choices=FileType.choices)