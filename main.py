import os
import re
import telebot
from playwright.sync_api import sync_playwright

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN do Telegram não definido")

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")


def extrair_menor_preco(texto):
    """
    Procura valores do tipo R$ 933, R$1.250, etc
    e retorna o menor encontrado
    """
    valores = re.findall(r"R\$\s?[\d\.]+", texto)
    precos = []

    for v in valores:
        numero = v.replace("R$", "").replace(".", "").strip()
        if numero.isdigit():
            precos.append(int(numero))

    return min(precos) if precos else None


@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 *Bot de voos ativo*\n\nUse /teste para buscar o menor preço REC ➜ FOR"
    )


@bot.message_handler(commands=["teste"])
def teste(msg):
    bot.send_message(msg.chat.id, "🔎 Buscando menor preço no Google Flights...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = (
            "https://www.google.com/travel/flights?"
            "q=Flights%20from%20REC%20to%20FOR"
        )

        page.goto(url)
        page.wait_for_timeout(12000)

        texto_pagina = page.inner_text("body")

        browser.close()

    menor_preco = extrair_menor_preco(texto_pagina)

    if menor_preco:
        bot.send_message(
            msg.chat.id,
            f"""🏷️ *Voo mais barato encontrado*

💰 *Preço:* ~R$ {menor_preco}

🔗 *Ver no Google Flights:*
{url}
"""
        )
    else:
        bot.send_message(
            msg.chat.id,
            "❌ Não consegui localizar preços no momento."
        )


if __name__ == "__main__":
    bot.infinity_polling()
