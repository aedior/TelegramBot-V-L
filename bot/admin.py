from django.contrib import admin
from bot.models import *

@admin.register(UserModel)
class UserPanel(admin.ModelAdmin):
    list_display = ["username", "telegram_user_num", "chat_id", "is_join", "is_admin", "can_add_admin"]
    list_filter = ["is_join", "is_admin", "can_add_admin"]


@admin.register(ChannelModel)
class ChannelPanel(admin.ModelAdmin):
    list_display = ["_channel_username"]
    
    
