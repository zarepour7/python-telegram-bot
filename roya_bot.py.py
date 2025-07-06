import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from config import TELEGRAM_TOKEN, OPENAI_API_KEY

# تنظیمات کلید API
openai.api_key = OPENAI_API_KEY

# فعال‌سازی لاگ برای خطایابی
logging.basicConfig(level=logging.INFO)

# فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات هوش مصنوعی هستم. سوالی داشتی بپرس!")

# دریافت پیام کاربر و ارسال پاسخ ChatGPT
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=500,
            temperature=0.7,
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {e}")

# اجرای ربات
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
