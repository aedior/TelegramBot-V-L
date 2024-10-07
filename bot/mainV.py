#import
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot
from pprint import pprint
from bot.models import UserModel, ChannelModel, PlaceInBot, VideoModel
from tBOT.settings import TELEGRAM_BOT_TOKEN_V, TELEGRAM_ADMIN_ID_V, TELEGRAM_CHANNEL_ID_V



#information
bot = TeleBot(token=TELEGRAM_BOT_TOKEN_V)
admin_id = TELEGRAM_ADMIN_ID_V
channel = TELEGRAM_CHANNEL_ID_V


#check channel for new post and send link
@bot.channel_post_handler(func=lambda msg: msg.sender_chat.id == channel, content_types=['audio', 'photo', 'voice', 'video', 'document',
                'text', 'location', 'contact', 'sticker'])
def sendlink(message):
    bot.send_message(chat_id=admin_id, text= f"https://t.me/testl_lbot?start={message.id}")

@bot.message_handler(content_types=['video'])
def sendVideo(message):
    bot.send_message(admin_id, f"{message.from_user.id, '@'+ message.from_user.username}")
    bot.send_video(admin_id, message.video.file_id)
    video, _ = VideoModel.objects.get_or_create(
        user_id = message.from_user.id ,
        user_username =  message.from_user.username,
        video_id = message.video.file_id
    )
    video.save()

#start whith link and forward video    
@bot.message_handler(commands=["start"], func=lambda msg:len(msg.text.split(" ")) > 1)
def sendData(message):
    post_id = message.text.split(" ")[-1]
    user, _ = UserModel.objects.get_or_create(
        telegram_user_num=message.from_user.id,
        chat_id=message.chat.id
    )
    user.username=message.from_user.username
    user.save()
    
    try:
        bot.forward_message(chat_id=user.chat_id, from_chat_id=channel, message_id=post_id, protect_content=False)
    except Exception as e:
        print(e)
        bot.reply_to(message, "پست مورد نظر یافت نشد.")



print("bot started")
bot.infinity_polling(interval=0, timeout=20)
