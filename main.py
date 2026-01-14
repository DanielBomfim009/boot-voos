import os
import telebot
from playwright.sync_api import sync_playwright

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 Bot ativo!\n\nUse /teste para simular uma busca de voo."
    )

@bot.message_handler(commands=["teste"])
def teste(msg):
    bot.send_message(msg.chat.id, "🔎 Abrindo Google Flights...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(
            "https://www.google.com/travel/flights?q=Flights%20from%20REC%20to%20FOR"
        )
        page.wait_for_timeout(10000)

        browser.close()

    bot.send_message(msg.chat.id, "✅ Página carregada com sucesso!")

if __name__ == "__main__":
    bot.infinity_polling()
