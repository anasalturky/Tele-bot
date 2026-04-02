import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# التوكن من متغيرات البيئة
TOKEN = os.getenv("8377790304:AAEYbz6ldbSysFg0b3PaLwAp3NGgdKvomAs")

# رقم التواصل
OWNER_NUMBER = "218946303497"
OWNER_WHATSAPP = f"https://wa.me/{OWNER_NUMBER}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """قائمة الترحيب والخدمات الرئيسية"""
    keyboard = [
        [InlineKeyboardButton("📺 اشتراكات", callback_data='subscriptions')],
        [InlineKeyboardButton("📱 سوشال ميديا", callback_data='social_media')],
        [InlineKeyboardButton("💳 فيزا إلكترونية", callback_data='visa')],
        [InlineKeyboardButton("🌐 تصميم موقع", callback_data='website')],
        [InlineKeyboardButton("📈 خدمات سوشال ميديا", callback_data='social_services')],
        [InlineKeyboardButton("🎮 شحن عملات", callback_data='coins')],
        [InlineKeyboardButton("💰 إضافة رصيد للمحفظة", callback_data='wallet')],
        [InlineKeyboardButton("📞 تواصل مع المالك", url=OWNER_WHATSAPP)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "👋 أهلاً بك في بوت Boosting Libya للخدمات الرقمية.\n\n"
        "يرجى اختيار الخدمة المطلوبة من القائمة أدناه:"
    )

    if update.message:
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ **مساعدة البوت**\n\n"
        "اختر القسم المطلوب من القائمة، ثم راجع الأسعار، وبعدها اضغط على زر التواصل لإتمام الشراء.\n\n"
        f"📞 رابط التواصل:\n{OWNER_WHATSAPP}"
    )
    await update.message.reply_text(text, parse_mode='Markdown')


async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📞 تواصل مع المالك مباشرة:\n{OWNER_WHATSAPP}")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الضغط على الأزرار"""
    query = update.callback_query
    await query.answer()

    back_button = [
        [InlineKeyboardButton("🔙 العودة للقائمة", callback_data='main_menu')],
        [InlineKeyboardButton("📞 شراء / تواصل", url=OWNER_WHATSAPP)]
    ]

    if query.data == 'subscriptions':
        text = (
            "📺 **الاشتراكات المتوفرة:**\n\n"
            "• نتفلكس 45 يوم ← 65 دينار\n"
            "• نتفلكس أسبوع ← 19 دينار\n"
            "• سناب بلس 3 أشهر ← 65 دينار\n"
            "• CapCut شهر ← 45 دينار\n"
            "• Canva شهر ← 20 دينار\n"
            "• ChatGPT شهر ← 70 دينار\n\n"
            f"📞 لإتمام الشراء تواصل مع المالك:\n{OWNER_WHATSAPP}"
        )

    elif query.data == 'social_media':
        text = (
            "📱 **خدمات السوشال ميديا:**\n\n"
            "• إعلان ممول اليوم ← 20 دينار\n"
            "• إنشاء بوت اشتراك شهري ← 150 دينار\n\n"
            f"📞 لإتمام الشراء تواصل مع المالك:\n{OWNER_WHATSAPP}"
        )

    elif query.data == 'visa':
        text = (
            "💳 **فيزا إلكترونية:**\n\n"
            "• فيزا إلكترونية ← تواصل لمعرفة التفاصيل والسعر النهائي\n\n"
            f"📞 لإتمام الشراء تواصل مع المالك:\n{OWNER_WHATSAPP}"
        )

    elif query.data == 'website':
        text = (
            "🌐 **تصميم موقع:**\n\n"
            "• تصميم موقع خدمات إلكترونية ← 250 دينار\n\n"
            f"📞 لإتمام الشراء تواصل مع المالك:\n{OWNER_WHATSAPP}"
        )

    elif query.data == 'social_services':
        text = (
            "📈 **خدمات سوشال ميديا:**\n\n"
            "• خدمات متنوعة للحسابات والصفحات\n"
            "• زيادة تفاعل ومتابعين وإعلانات\n"
            "• تواصل لتحديد الطلب بالتفصيل\n\n"
            f"📞 لإتمام الشراء تواصل مع المالك:\n{OWNER_WHATSAPP}"
        )

    elif query.data == 'coins':
        text = (
            "🎮 **شحن العملات والبطاقات:**\n\n"
            "**شدات ببجي:**\n"
            "• 60 شدة ← 12.7 دينار\n"
            "• 325 شدة ← 59.7 دينار\n"
            "• 660 شدة ← 117.7 دينار\n"
            "• 1800 شدة ← 293.5 دينار\n\n"
            "**كروت آيتونز تركي:**\n"
            "• 25 TL ← 8.9 دينار\n"
            "• 50 TL ← 17.6 دينار\n"
            "• 100 TL ← 33.5 دينار\n"
            "• 250 TL ← 82 دينار\n\n"
            "**كروت آيتونز أمريكي:**\n"
            "• 2$ ← 25.5 دينار\n"
            "• 5$ ← 64 دينار\n\n"
            f"📞 لإتمام الشراء تواصل مع المالك:\n{OWNER_WHATSAPP}"
        )

    elif query.data == 'wallet':
        text = (
            "💰 **إضافة رصيد للمحفظة:**\n\n"
            "• يتم الشحن عن طريق **دفع ليبيانا**\n"
            "• أرسل قيمة الرصيد المطلوبة لإتمام العملية\n\n"
            f"📞 لإتمام الشراء تواصل مع المالك:\n{OWNER_WHATSAPP}"
        )

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


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling an update:", exc_info=context.error)


def main():
    """تشغيل البوت"""
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is not set.")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    print("البوت يعمل الآن...")
    application.run_polling()


if __name__ == '__main__':
    main()
