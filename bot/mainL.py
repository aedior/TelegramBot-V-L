import telebot
from bot.models import UserModel, ChannelModel, PlaceInBot
from bot.messages import *
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from tBOT.settings import TELEGRAM_BOT_TOKEN_L
from bot.helper import *


TOKEN = TELEGRAM_BOT_TOKEN_L

# لیست کانال‌های اجباری و شناسه‌های کاربران
required_channels = [c.channel_username for c in ChannelModel.objects.all()]


# ایجاد ربات
bot = telebot.TeleBot(TOKEN)



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
        user = getUser(call.message, bot)

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
                keyboard.add(InlineKeyboardButton(text="حذف چنل اسپانسر", callback_data="delete"))
                for c in required_chann:
                    keyboard.add(InlineKeyboardButton(text=c, callback_data=c))
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
                checkInChannels(user, bot)
                if user.is_join:
                    bot.delete_message(user.chat_id, call.message.message_id, 2)
                    if user.postId == 0:
                        bot.send_message(user.chat_id, welcome_user)
                    else:
                        showPost(user, bot)
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
            case _:
                channel_id = call.data
                count = bot.get_chat_member_count(channel_id)
                ChannelModel.objects.get_or_create(
                    _channel_username = channel_id.split("@")
                )
                countR = count - ChannelModel.users
                user
                bot.send_message(call.message.chat.id, f"تعداد عضوشدگان {channel_id}: \n {countR}")
                
                    

def start_admin(message, user):
        
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
    startText = message.text.split(" ")
    user = getUser(message, bot)
    
    if len(startText) > 1:
        post_id = startText[-1]
        user.postId = post_id
        user.save()
        checkInChannels(user, bot)
        if user.is_join:
            showPost(user, bot)
        else:
            start_user(message, user)
        
    else:
        checkInChannels(user, bot)
        
        if user.is_admin:
            start_admin(message, user)
            return
        start_user(message, user)



# تابع چک کردن عضویت
@bot.message_handler(func=lambda message: True)
def check_membership(message):
    user =  getUser(message)

    
    if user.can_add_admin and user.placeInBot == PlaceInBot.ADD_ADMIN:
        try:
            adminID = int(message.text)
        except:
            return bot.reply_to(message, "لطفا آیدی عددی ادمین را وارد کنید")
        
        try:
            admin=UserModel.objects.get(
                chat_id = adminID
            )
        except:
            return bot.reply_to(message, "این ایدی عددی یافت نشد.")
        
        admin.is_admin = True
        admin.save()
        bot.reply_to(message, "این آیدی ذخیره شد")
        
    if user.placeInBot == PlaceInBot.ADD_CHANNEL:
        try:
            count = bot.get_chat_member_count(f"@{message.text}")
            channelcount=ChannelModel(users=count)
            channeladd=ChannelModel(_channel_username=message.text)
            channeladd.save()
            channelcount.save()
            bot.reply_to(message, "کانال مورد نظر در لیست اسپانسر ها اضافه شد")
            
        except Exception as e:
            print(e)
            return bot.reply_to(message, "کانال مورد نظر یافت نشد")
            
            
    if user.placeInBot == PlaceInBot.DELET_CHANNEL:
        try:
            channeldel=ChannelModel.objects.get(
                _channel_username=message.text
            )
            channeldel.delete()
            bot.reply_to(message, "کانال مورد نظر در لیست اسپانسر ها حذف شد")
            
        except Exception as e:
            print(e)
            return bot.reply_to(message, "کانال مورد نظر یافت نشد")
            
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
            return bot.reply_to(message, " خطایی رخ داده است")

    if user.placeInBot == PlaceInBot.DELETE_ADMIN:
        try:
            adminID = int(message.text)
        except:
            return bot.reply_to(message, "لطفا آیدی عددی ادمین را وارد کنید")
        
        try:
            admin=UserModel.objects.get(
                chat_id = adminID
            )
        except:
            return bot.reply_to(message, "این ایدی عددی یافت نشد.")
        
        admin.is_admin = False
        admin.save()
        bot.reply_to(message, "این آیدی دیگر ادمین نیست")
        
    user.placeInBot = 0
    user.save()
        
# راه‌اندازی ربات
print("bot started ...")
bot.infinity_polling(interval=0, timeout=20)
