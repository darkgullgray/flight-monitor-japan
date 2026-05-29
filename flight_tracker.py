from playwright.sync_api import sync_playwright
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

FROM_EMAIL = "ettciu@gmail.com"
APP_PASSWORD = "qrrn gpba imjt skgb"
TO_EMAIL = "ettciu@gmail.com"

URL = "https://www.google.com/travel/flights"


def get_flight_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL)

        page.wait_for_timeout(10000)

        content = page.content()

        browser.close()

       import csv
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

with open("prices.csv", "a", newline="", encoding="utf-8") as f:
writer = csv.writer(f)
writer.writerow([
today,
"ROMA-OSAKA",
1800,
"TEST AIRLINE"
])

return "Storico aggiornato correttamente"



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
