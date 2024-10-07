import telebot
from bot.models import UserModel, ChannelModel
from bot.messages import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def showPost(user, bot):
    keyboard=InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="مشاهده", url=f"https://t.me/badiidaaybot?start={user.postId}"))
    bot.send_message(user.chat_id, text="از گزینه های زیر استفاده نمایید", reply_markup=keyboard)

def getUser(message):
    
    user, _ = UserModel.objects.get_or_create(
        chat_id=message.chat.id,
    )
    user.username=message.from_user.username
    user.save()
    
    return user

def checkInChannels(user: UserModel, bot):
    isJoined = True
    for channel in [c.channel_username for c in ChannelModel.objects.all()]:
        try:
            getMember=bot.get_chat_member(channel, user.chat_id)
            if getMember.status == 'left':
                isJoined = False
                
        except Exception as e:
            print(e)
            isJoined = False
            break
    user.is_join = isJoined
    user.save()
