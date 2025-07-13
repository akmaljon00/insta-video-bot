import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = "7632418848:AAEg81huvk_sVLxmAO8khzAO7GvY_7OP0iA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Привет! Отправь ссылку на Instagram-видео, и я пришлю тебе ссылку на скачивание.")

@bot.message_handler(func=lambda message: 'instagram.com' in message.text)
def download_instagram(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "🔍 Обрабатываю ссылку, подожди...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "url": url,
            "submit": ""
        }

        response = requests.post("https://snapinsta.app/action.php", data=data, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        download_link = soup.find("a", {"target": "_blank"})

        if download_link and download_link["href"].startswith("http"):
            bot.send_message(message.chat.id, f"✅ Вот твоё видео:\n{download_link['href']}")
        else:
            bot.send_message(message.chat.id, "❌ Не удалось найти видео. Возможно, ссылка неправильная или пост приватный.")

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка при скачивании: {e}")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправь ссылку на Instagram Reel или видео.")

bot.polling()
