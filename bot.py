import telebot
import requests
from telebot import types
import random
import time
import os
import threading
from datetime import datetime, timedelta

API_TOKEN = '8377790304:AAEYbz6ldbSysFg0b3PaLwAp3NGgdKvomAs'
SMM_API_KEY = ''
SMM_API_URL = ''

bot = telebot.TeleBot(8377790304:AAEYbz6ldbSysFg0b3PaLwAp3NGgdKvomAs)

spin_lock = threading.Lock()
DB_FILE = "spin_history.txt"
memory_cache = {}

WHATSAPP_URL = "https://wa.me/218946303497"

# ✅ الأسعار الجديدة
PRICES_TEMPLATE = """
📊 أسعار خدمات السوشال ميديا

🔵 Facebook:
• 1000 متابع ← 10 دينار
• 1000 لايك ← 5 دينار
• 1000 مشاهدة ← 3 دينار

📸 Instagram:
• 1000 متابع ← 15 دينار
• 1000 لايك ← 5 دينار
• 1000 مشاهدة ← 3 دينار

🎵 TikTok:
• 1000 متابع ← 19 دينار
• 1000 لايك ← 5 دينار
• 1000 مشاهدة ← 3 دينار
"""

SUBSCRIPTIONS_TEXT = """💎 الاشتراكات

• نتفلكس 45 يوم ← 65 دينار
• نتفلكس أسبوع ← 19 دينار
• سناب بلس 3 أشهر ← 65 دينار
• CapCut شهر ← 45 دينار
• Canva شهر ← 20 دينار
• ChatGPT شهر ← 70 دينار
"""

SOCIAL_MEDIA_TEXT = """📱 خدمات السوشال ميديا

• إعلان ممول يوم ← 20 دينار
• إنشاء بوت اشتراك شهري ← 150 دينار
"""

PRIZES_DATA = [
    {"text": "❌ حظ أوفر المرة القادمة", "weight": 40},
    {"text": "🎁 مبروك! 100 لايك إنستجرام", "weight": 25},
    {"text": "🎁 خصم 10%", "weight": 15},
    {"text": "🎁 500 مشاهدة تيك توك", "weight": 14},
    {"text": "🎁 200 لايك فيسبوك", "weight": 5},
    {"text": "👑 1000 متابع إنستجرام", "weight": 1}
]

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        for line in f:
            try:
                uid, l_time = line.strip().split("|")
                memory_cache[int(uid)] = datetime.strptime(l_time, "%Y-%m-%d %H:%M:%S")
            except:
                continue

# القائمة الرئيسية
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("♻️ إعادة التعبئة", callback_data="refill"),
        types.InlineKeyboardButton("🎡 عجلة الحظ", callback_data="spin"),
        types.InlineKeyboardButton("📊 الأسعار", callback_data="prices"),
        types.InlineKeyboardButton("💎 الاشتراكات", callback_data="subs"),
        types.InlineKeyboardButton("📱 خدمات إضافية", callback_data="social"),
        types.InlineKeyboardButton("📞 تواصل واتساب", url=WHATSAPP_URL)
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "اهلا بك في بوت سوشال ليبيا 👑🔥\n\nاختر من القائمة 👇",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    # 🎡 عجلة الحظ
    if call.data == "spin":
        with spin_lock:
            now = datetime.now()
            if chat_id in memory_cache:
                if now < memory_cache[chat_id] + timedelta(hours=24):
                    bot.answer_callback_query(
                        call.id,
                        "يمكنك المحاولة بعد 24 ساعة ❌",
                        show_alert=True
                    )
                    return

            memory_cache[chat_id] = now
            with open(DB_FILE, "a") as f:
                f.write(f"{chat_id}|{now.strftime('%Y-%m-%d %H:%M:%S')}\n")

        bot.delete_message(chat_id, msg_id)
        wait = bot.send_message(chat_id, "🎡 جاري التدوير... انتظر عزيزي الزبون")

        time.sleep(2)

        res = random.choices(
            [p["text"] for p in PRIZES_DATA],
            weights=[p["weight"] for p in PRIZES_DATA],
            k=1
        )[0]

        bot.edit_message_text(
            f"🎉 النتيجة:\n\n{res}",
            chat_id,
            wait.message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🔙 رجوع", callback_data="back")
            )
        )

    # 📊 الأسعار
    elif call.data == "prices":
        bot.edit_message_text(
            PRICES_TEMPLATE,
            chat_id,
            msg_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🔙 رجوع", callback_data="back")
            )
        )

    # 💎 الاشتراكات
    elif call.data == "subs":
        bot.edit_message_text(
            SUBSCRIPTIONS_TEXT,
            chat_id,
            msg_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🔙 رجوع", callback_data="back")
            )
        )

    # 📱 خدمات إضافية
    elif call.data == "social":
        bot.edit_message_text(
            SOCIAL_MEDIA_TEXT,
            chat_id,
            msg_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🔙 رجوع", callback_data="back")
            )
        )

    # ♻️ refill
    elif call.data == "refill":
        msg = bot.send_message(chat_id, "أرسل رقم الطلب عزيزي الزبون 🔄")
        bot.register_next_step_handler(msg, process_refill)

    elif call.data == "back":
        bot.edit_message_text(
            "اهلا بك في بوت سوشال ليبيا 👑🔥\n\nاختر من القائمة 👇",
            chat_id,
            msg_id,
            reply_markup=main_menu()
        )

def process_refill(message):
    if message.text and message.text.isdigit():
        bot.reply_to(message, "جاري التحقق...")

        payload = {'key': SMM_API_KEY, 'action': 'refill', 'order': message.text}

        try:
            r = requests.post(SMM_API_URL, data=payload).json()
            if 'refill' in r:
                bot.reply_to(message, "تم إرسال الطلب ✅")
            else:
                bot.reply_to(message, "رقم غير صالح ❌")
        except:
            bot.reply_to(message, "خطأ في الاتصال ❌")
    else:
        bot.reply_to(message, "أدخل أرقام فقط ❌")

@bot.message_handler(func=lambda m: True)
def other(message):
    bot.send_message(
        message.chat.id,
        "⚠️ عزيزي الزبون، اختر من القائمة 👇",
        reply_markup=main_menu()
    )

if __name__ == "__main__":
    bot.infinity_polling()
