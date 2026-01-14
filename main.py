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
    Extrai valores monetários do tipo R$ 933, R$1.250 etc
    e retorna o menor encontrado
    """
    valores = re.findall(r"R\$\s?\d[\d\.]*", texto)
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
        "🤖 *Bot de Voos Ativo*\n\nUse /teste para buscar um voo real com data definida."
    )


@bot.message_handler(commands=["teste"])
def teste(msg):
    bot.send_message(msg.chat.id, "🔎 Buscando menor preço com data definida...")

    # EXEMPLO FIXO (REC ➜ FOR)
    origem = "rec"
    destino = "for"
    ida = "260128"     # 28/01/2026
    volta = "260131"   # 31/01/2026

    url = (
        f"https://www.google.com/travel/flights/"
        f"search?tfs=CBwQAhokEgoyMDI2LTAxLTI4agcIARIDUkVD"
        f"cgcIARIDRk9SGhQKAiABEgoyMDI2LTAxLTMxagcIARIDRk9S"
        f"cgcIARIDUkVDEAFAAUgBmAEC"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)
        page.wait_for_timeout(15000)

        texto = page.inner_text("body")

        browser.close()

    menor_preco = extrair_menor_preco(texto)

    if menor_preco:
        bot.send_message(
            msg.chat.id,
            f"""🏷️ *Voo mais barato encontrado*

🛫 *Origem:* Recife (REC)
🛬 *Destino:* Fortaleza (FOR)

📆 *Ida:* 28/01/2026
📆 *Volta:* 31/01/2026

💰 *Preço:* ~R$ {menor_preco}

🔗 *Ver no Google Flights:*
{url}
"""
        )
    else:
        bot.send_message(
            msg.chat.id,
            "❌ Não consegui localizar preços para esse filtro."
        )


if __name__ == "__main__":
    bot.infinity_polling()
