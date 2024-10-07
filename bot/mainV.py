#import
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot
from pprint import pprint
from bot.models import UserModel, ChannelModel, PlaceInBot, FileType, FileModel
from tBOT.settings import TELEGRAM_BOT_TOKEN_V, TELEGRAM_ADMIN_ID_V, TELEGRAM_CHANNEL_ID_V
from bot.helper import *
from time import sleep



#information
bot = TeleBot(token=TELEGRAM_BOT_TOKEN_V)
admin_id = TELEGRAM_ADMIN_ID_V
channel = TELEGRAM_CHANNEL_ID_V


#check channel for new post and send link
@bot.channel_post_handler(func=lambda msg: msg.sender_chat.id == channel, content_types=['audio', 'photo', 'voice', 'video', 'document',
                'text', 'location', 'contact', 'sticker'])
def sendlink(message):
    bot.send_message(chat_id=admin_id[0], text= f"https://t.me/waitingggbot?start={message.id}")


# @bot.message_handler(content_types=['video'])
# def sendVideo(message):
#     user = getUser(message, bot)
#     for admin in admin_id:
#         bot.send_message(admin, f"{user.chat_id}, {user.username}")
#         bot.send_video(admin, message.video.file_id)
#     video, _ = VideoModel.objects.get_or_create(
#         user_id = message.from_user.id ,
#         user_username =  message.from_user.username,
#         video_id = message.video.file_id
#     )
#     video.save()

@bot.message_handler(content_types=['photo', 'video'])
def sendphoto(message):
    
    # set data
    user = getUser(message, bot)
    
    # set conntent type to file
    if message.content_type == "photo":
        file = message.photo[-1]
        file_type = FileType.PHOTO
        send = bot.send_photo
    elif message.content_type == "video":
        file = message.video
        file_type = FileType.VIDEO
        send = bot.send_video
    else:
        raise ValueError(f"content type {message.content_type} not set in models")
    
    # send to admins
    for admin in admin_id:
        bot.send_message(admin, f"{user.chat_id}, {user.username}")
        send(admin, file.file_id)
    photo, _ = FileModel.objects.get_or_create(
        user=user,
        hash_id = file.file_id,
        file_type=file_type
    )
    photo.save()

#start whith link and forward video    
@bot.message_handler(commands=["start"], func=lambda msg:len(msg.text.split(" ")) > 1)
def sendData(message):
    post_id = message.text.split(" ")[-1]
    user = getUser(message, bot)
    try:
        msg = bot.copy_message(chat_id=user.chat_id, from_chat_id=channel, message_id=post_id, protect_content=False)
        bot.send_message(user.chat_id, "این پیام بعد از 3 ثانیه حذف خواهد شد.")
        bot.delete_message(user.chat_id, msg.message_id, 3)
    except Exception as e:
        print(e)
        bot.reply_to(message, "پست مورد نظر یافت نشد.")



print("bot started")
bot.infinity_polling(interval=0, timeout=20)
