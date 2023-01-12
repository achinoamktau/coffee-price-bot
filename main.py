import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

TARGET_PRICE = 300
load_dotenv()
EMAIL = "email"
PASS = "pass"
EMAIL_TO = "email"


def send_email(total, link):
    global EMAIL_TO, EMAIL, PASS
    sub = "Amazon Price Alert!!!"
    message = f"The coffee maker you wanted is now only {total}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()   # encrypt
        connection.login(user=EMAIL, password=PASS)  # login to the email that is sending the message
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL_TO, msg=f"Subject: {sub}\n\n{message}\n{link}")


amz_url = "https://www.amazon.co.uk/Nespresso-Creatista-Brushed-Stainless-Steel/dp/B01NGTI2JU/ref=lp_193679031_1_1"
response = requests.get(url=amz_url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
})
response.raise_for_status()
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

price = soup.select(".a-price-whole")[0].getText().strip(".")
price_prac = soup.select(".a-price-fraction")[0].getText()
price = int(price)
price_prac = int(price_prac)
total = price + price_prac / 100


if total < TARGET_PRICE:
    send_email(total, amz_url)



