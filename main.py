from playwright.sync_api import sync_playwright
import re
import time

URL = "https://www.google.com/travel/flights?q=Flights%20from%20REC%20to%20FOR%202026-01-28%20return%202026-01-31"

def extrair_menor_preco():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)

        # Aguarda carregamento real
        page.wait_for_timeout(10000)

        html = page.content()

        # Regex REAL usada por bots (não seletor)
        precos = re.findall(r'R\$\s?\d{1,3}(?:\.\d{3})*,\d{2}', html)

        browser.close()

        if not precos:
            return None

        # Converte para float e pega o menor
        valores = [
            float(p.replace("R$", "").replace(".", "").replace(",", "."))
            for p in precos
        ]

        return min(valores)

if __name__ == "__main__":
    preco = extrair_menor_preco()

    if preco:
        print(f"💰 Menor preço encontrado: R$ {preco:.2f}")
    else:
        print("❌ Não foi possível localizar preço")
