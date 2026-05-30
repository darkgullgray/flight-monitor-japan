from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

FROM_EMAIL = "ettciu@gmail.com"
APP_PASSWORD = "qrrn gpba imjt skgb"
TO_EMAIL = "ettciu@gmail.com"

def get_flight_price():
    test_url = "https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI2LTExLTAyagcIARIDRkNPcgcIARIDS0lYGh4SCjIwMjYtMTEtMTZqBwgBEgNLSVhyBwgBEgNGQ09AAUABQAFIAXABggELCP___________wGYAQE&hl=it&gl=IT"
    milano_osaka_url = "https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI2LTExLTAyagcIARIDTVhQcgcIARIDS0lYGh4SCjIwMjYtMTEtMTZqBwgBEgNLSVhyBwgBEgNNWFBAAUABQAFIAXABggELCP___________wGYAQE&tfu=EgYIABAAGAA&hl=it&gl=IT"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(test_url, wait_until="networkidle")
        page.wait_for_timeout(10000)

        testo = page.locator("body").inner_text()
        testo_roma = testo

        page.goto(milano_osaka_url, wait_until="networkidle")
        page.wait_for_timeout(10000)

        testo_milano = page.locator("body").inner_text()
        browser.close()

        prezzo = "Non trovato"
        valutazione = "Non trovata"

        righe = testo_roma.split("\n")

        for riga in righe:
            if "da " in riga and "€" in riga:
                prezzo = riga.strip()
                break

        for riga in righe:
            if "Al momento, i prezzi" in riga:
                valutazione = riga.strip()
                break
            
        prezzo_milano = "Non trovato"
        valutazione_milano = "Non trovata"

        righe_milano = testo_milano.split("\n")

        for riga in righe_milano:
            if "da " in riga and "€" in riga:
                prezzo_milano = riga.strip()
                break

        for riga in righe_milano:
            if "Al momento, i prezzi" in riga:
                valutazione_milano = riga.strip()
                break
        
        report = f"""

        ROMA → OSAKA

        Prezzo minimo:
        {prezzo}

        Valutazione Google:
        {valutazione}
        
        MILANO → OSAKA

        Prezzo minimo:
        {prezzo_milano}

        Valutazione Google:
        {valutazione_milano}
        """

        return report

price = get_flight_price()

message = f"""
Monitor voli Giappone

Data: {datetime.now()}

Risultato:
{price}
"""

msg = MIMEText(message)
msg["Subject"] = "Report voli Giappone"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(FROM_EMAIL, APP_PASSWORD)
server.send_message(msg)
server.quit()

print("Email inviata")
