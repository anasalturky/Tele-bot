import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ضع التوكن الخاص بك هنا
TOKEN = '8377790304:AAEYbz6ldbSysFg0b3PaLwAp3NGgdKvomAs'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """قائمة الترحيب والخدمات الرئيسية"""
    keyboard = [
        [InlineKeyboardButton("💎 عملات تيك توك", callback_data='tiktok_coins')],
        [InlineKeyboardButton("💳 فيزا إلكترونية", callback_data='visa')],
        [InlineKeyboardButton("💙 خدمات فيسبوك", callback_data='facebook')],
        [InlineKeyboardButton("📸 خدمات إنستقرام", callback_data='instagram')],
        [InlineKeyboardButton("🎬 متابعين تيك توك", callback_data='tiktok_followers')],
        [InlineKeyboardButton("🎮 شحن ألعاب وتطبيقات", callback_data='games')],
        [InlineKeyboardButton("📞 تواصل مع المالك", url='https://wa.me/218946303497')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = "👋 أهلاً بك في بوت Boosting Libya للخدمات الرقمية.\n\nيرجى اختيار الخدمة المطلوبة من القائمة أدناه:"

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text(
            welcome_text,
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الضغط على الأزرار"""
    query = update.callback_query
    await query.answer()

    back_button = [[InlineKeyboardButton("🔙 العودة للقائمة", callback_data='main_menu')]]

    if query.data == 'tiktok_coins':
        text = (
            "💰 **أسعار عملات تيك توك:**\n"
            "• 30 عملة ← 7 دينار\n"
            "• 100 عملة ← 19 دينار\n"
            "• 350 عملة ← 60 دينار\n"
            "• 1000 عملة ← 155 دينار"
        )

    elif query.data == 'visa':
        text = "💳 **فيزا إلكترونية:**\nصلاحية 3 سنوات السعر: 200 دينار."

    elif query.data == 'facebook' or query.data == 'instagram':
        platform = "فيسبوك" if query.data == 'facebook' else "إنستقرام"
        text = (
            f"📈 **خدمات {platform}:**\n"
            "• 1000 متابع ← 15 دينار\n"
            "• 1000 لايك ← 5 دينار\n"
            "• 1000 مشاهدة ← 3 دينار"
        )

    elif query.data == 'tiktok_followers':
        text = "👥 **متابعين تيك توك:**\n• 1000 متابع ← 18 دينار"

    elif query.data == 'games':
        text = "🎮 **شحن الألعاب والتطبيقات:**\nمتوفر شحن جميع الألعاب. أرسل اسم التطبيق وصورته للمالك لتأكيد الطلب."

    elif query.data == 'main_menu':
        await start(update, context)
        return

    else:
        text = "حدث خطأ، حاول مرة أخرى."

    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(back_button),
        parse_mode='Markdown'
    )

def main():
    """تشغيل البوت"""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("البوت يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
