from playwright.sync_api import sync_playwright
import re

URL = "https://www.google.com/travel/flights?q=Flights%20from%20REC%20to%20FOR%202026-01-28%20return%202026-01-31"

def extrair_menor_preco():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🌐 Acessando Google Flights...")
        page.goto(URL, timeout=60000)

        print("⏳ Aguardando carregamento da página...")
        page.wait_for_timeout(12000)

        html = page.content()

        # Regex que captura preços reais exibidos
        precos = re.findall(r'R\$\s?\d{1,3}(?:\.\d{3})*,\d{2}', html)

        browser.close()

        if not precos:
            return None

        valores = [
            float(p.replace("R$", "").replace(".", "").replace(",", "."))
            for p in precos
        ]

        return min(valores)

if __name__ == "__main__":
    preco = extrair_menor_preco()

    if preco:
        print(f"✅ MENOR PREÇO ENCONTRADO: R$ {preco:.2f}")
    else:
        print("❌ NÃO FOI POSSÍVEL LOCALIZAR PREÇO")
