import telebot
from bot.models import UserModel, ChannelModel, PlaceInBot
from bot.messages import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from tBOT.settings import TELEGRAM_BOT_TOKEN_L


TOKEN = TELEGRAM_BOT_TOKEN_L

# لیست کانال‌های اجباری و شناسه‌های کاربران
required_channels = [c.channel_username for c in ChannelModel.objects.all()]


# ایجاد ربات
bot = telebot.TeleBot(TOKEN)


def checkInChannels(user: UserModel):
    isJoined = True
    for channel in [c.channel_username for c in ChannelModel.objects.all()]:
        try:
            getMember=bot.get_chat_member(channel, user.telegram_user_num)
            if getMember.status == 'left':
                isJoined = False
                
        except Exception as e:
            print(e)
            isJoined = False
            break
    user.is_join = isJoined
    user.save()



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    
        user = UserModel.objects.get(
            telegram_user_num=call.message.chat.id
        )
        match call.data:
            case "count":
                countuser = UserModel.objects.all().count()
                bot.send_message(user.chat_id, f"تعداد کاربران-->{countuser}")
            case "add_admin":
                bot.send_message(user.chat_id, "لطفا ایدی عددی فرد مورد نظر را ارسال نمیایید.")
                user.placeInBot = PlaceInBot.ADD_ADMIN
                user.save()
            case "delete_admin":
                bot.send_message(user.chat_id, "لطفا ایدی عددی فرد مورد نظر را ارسال نمیایید.")
                user.placeInBot = PlaceInBot.DELETE_ADMIN
                user.save()
            case "channel":
                required_chann = [c.channel_username for c in ChannelModel.objects.all()]
                
                keyboard=InlineKeyboardMarkup(row_width=1)
                keyboard.add(InlineKeyboardButton(text="اضافه کردن اسپانسر", callback_data="add_channel"))
                for c in required_chann:
                    keyboard.add(InlineKeyboardButton(text=c, callback_data='delete'))
                bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=keyboard)
            case "add_channel":
                bot.send_message(user.chat_id, "لطفا ایدی کانال مورد نظر را بدون (@) ارسال نمیایید.")
                user.placeInBot = PlaceInBot.ADD_CHANNEL
                user.save()
            case "delete":
                bot.send_message(user.chat_id, " برای حذف شدن از لیست لطفا ایدی کانال مورد نظر را بدون (@) ارسال نمیایید.")
                user.placeInBot = PlaceInBot.DELET_CHANNEL
                user.save()
            case "join":
                checkInChannels(user)
                if user.is_join:
                    bot.delete_message(user.chat_id, call.message.message_id, 2)
                    if user.postId == 0:
                        bot.send_message(user.chat_id, welcome_user)
                    else:
                        keyboard.add(InlineKeyboardButton(text="مشاهده", url=f"https://t.me/badiidaaybot?start={user.postId}"))
                else:
                    bot.answer_callback_query(call.id, text="شما عضو چنل ها نیستید", show_alert=True)
            case "all_message":
                bot.send_message(user.chat_id, "لطفا پیام همگانی خود را در قالب یک متن نوشته و ارسال کنید")
                user.placeInBot = PlaceInBot.ALL_MESSAGE
                user.save()
            case "admins":
                admis = [UserModel.objects.get(
                    is_admin=True
                )]
                keyboard=InlineKeyboardMarkup(row_width=1)
                keyboard.add(InlineKeyboardButton(text="اضافه کردن اسپانسر", callback_data="add_admin"))
                for a in admis:
                    keyboard.add(InlineKeyboardButton(text=a, callback_data='delete_admin'))
                bot.edit_message_reply_markup(call.from_user.id, call.message.message_id, reply_markup=keyboard)

                
                    
                    
                
                
                
                
        
        

def start_admin(message, user):
    user = UserModel.objects.get(
        telegram_user_num=message.from_user.id
    )
    
    keyboard= InlineKeyboardMarkup(row_width=1)
    a=InlineKeyboardButton(text="تعداد یوزر", callback_data="count")
    b=InlineKeyboardButton(text="ادمین", callback_data="admins")
    c=InlineKeyboardButton(text="کانال های اسپاسنر", callback_data="channel")
    d=InlineKeyboardButton(text="  پیام همگانی", callback_data="all_message")
    
    
    if user.can_add_admin:
        keyboard.add(a,b,c,d)
    else:    
        keyboard.add(a,c,d)
    bot.send_message(chat_id=user.chat_id,text="سلام لطفا یکی از گزینه هارا انتخاب کنید", reply_markup=keyboard)
    
def start_user(message, user):
    
    if user.is_join:
        bot.reply_to(message, welcome_user)
    else:
        keyboard=InlineKeyboardMarkup(row_width=1)
        for c in ChannelModel.objects.all():
                    keyboard.add(InlineKeyboardButton(text=c.channel_username, url=f"https://t.me/{c._channel_username}"))
        keyboard.add(InlineKeyboardButton(text="عضو شدم", callback_data="join"))
        bot.send_message(chat_id=user.chat_id, text=welcome_messages, reply_markup=keyboard)
    


# تابع شروع
@bot.message_handler(commands=['start'])
def start(message):
    userCount = UserModel.objects.all().count()
    user, _ = UserModel.objects.get_or_create(
        telegram_user_num=message.from_user.id,
        chat_id=message.chat.id
    )
    user.username=message.from_user.username
    user.save()
    
    if len(message.text.split(" ")) > 1:
        
        UserModel.objects.get_or_create(
            telegram_user_num = message.from_user.id,
            postId = message.text.split(" ")[-1]
        )
        checkInChannels(user)
        if user.is_join:
            post_id = message.text.split(" ")[-1]
            keyboard=InlineKeyboardMarkup(row_width=1)
            keyboardg = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(InlineKeyboardButton(text="مشاهده", url=f"https://t.me/badiidaaybot?start={post_id}"))
            bot.send_message(user.chat_id, text="از گزینه های زیر استفاده نمایید", reply_markup=keyboard)
            
        else:
            start_user(message, user)
        
    else:
        checkInChannels(user)
        
        if user.is_admin:
            start_admin(message, user)
            return
        start_user(message, user)



# تابع چک کردن عضویت
@bot.message_handler(func=lambda message: True)
def check_membership(message):
    user = UserModel.objects.get(
        telegram_user_num=message.from_user.id
    )
    
    if user.can_add_admin and user.placeInBot == PlaceInBot.ADD_ADMIN:
        try:
            adminID = int(message.text)
        except:
            return bot.reply_to(message, "لطفا آیدی عددی ادمین را وارد کنید")
        
        try:
            admin=UserModel.objects.get(
                telegram_user_num = adminID
            )
        except:
            return bot.reply_to(message, "این ایدی عددی یافت نشد.")
        
        admin.is_admin = True
        admin.save()
        bot.reply_to(message, "این آیدی ذخیره شد")
        
    if user.placeInBot == PlaceInBot.ADD_CHANNEL:
        try:
            channeladd=ChannelModel(_channel_username=message.text)
            channeladd.save()
            bot.reply_to(message, "کانال مورد نظر در لیست اسپانسر ها اضافه شد")
            
        except Exception as e:
            print(e)
            
            
    if user.placeInBot == PlaceInBot.DELET_CHANNEL:
        try:
            channeldel=ChannelModel.objects.get(
                _channel_username=message.text
            )
            channeldel.delete()
            bot.reply_to(message, "کانال مورد نظر در لیست اسپانسر ها حذف شد")
            
        except Exception as e:
            print(e)
            
    if user.placeInBot == PlaceInBot.ALL_MESSAGE:
        try:
            allmsg=[c.chat_id for c in UserModel.objects.all()]
            for u in allmsg:
                try:
                    bot.send_message(u, text=message.text)
                except Exception as e:
                    print(e)
                    continue
            bot.reply_to(message, "ارسال شد")
            
        except Exception as e:
            print(e)
            bot.reply_to(message, " خطایی رخ داده است")

    if user.placeInBot == PlaceInBot.DELETE_ADMIN:
        try:
            adminID = int(message.text)
        except:
            return bot.reply_to(message, "لطفا آیدی عددی ادمین را وارد کنید")
        
        try:
            admin=UserModel.objects.get(
                telegram_user_num = adminID
            )
        except:
            return bot.reply_to(message, "این ایدی عددی یافت نشد.")
        
        admin.is_admin = False
        admin.save()
        bot.reply_to(message, "این آیدی دیگر ادمین نیست")
        
            
            
# راه‌اندازی ربات
print("bot started ...")
bot.polling(none_stop=True)
