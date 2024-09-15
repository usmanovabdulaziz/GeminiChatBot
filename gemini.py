from dotenv import load_dotenv
import os
import telebot
import google.generativeai as genai

# .env faylini yuklaymiz
load_dotenv()

# API kalitlarni os.environ orqali yuklaymiz
bot_api_key = os.getenv("TELEGRAM_API_KEY")
gemini_api_key = os.getenv("GEMINAI_API_KEY")

# Telegram botini API kaliti bilan ishga tushiramiz
bot = telebot.TeleBot(bot_api_key, parse_mode=None)

# Gemini AI uchun konfiguratsiya qilamiz
genai.configure(api_key=gemini_api_key)

# GeminAI uchun boshqa kodlar
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(user_message)
    bot.reply_to(message, response.text)

bot.infinity_polling()
