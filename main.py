from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from datetime import datetime


def check_rates():
    chrome_driver_path = "/Users/maxon462/Downloads/chrome-mac-arm64/chromedriver"
    chrome_binary_path = "/Users/maxon462/Downloads/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"

    chrome_options = Options()
    chrome_options.binary_location = chrome_binary_path
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://p2p.binance.com/en/trade/sell/USDT?fiat=PLN&payment=all-payments"

    driver.get(url)
    time.sleep(5)
    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    maxauto_rate = None

    ads = soup.find_all('div', class_='bn-flex PaymentMethodList')

    for ad in ads:
        try:
            nickname_tag = ad.find_previous('a', class_='bn-balink')
            if not nickname_tag:
                continue
            nickname = nickname_tag.text.strip()

            payment_methods_elements = ad.find_all('div', class_='PaymentMethodItem__text')
            payment_methods = [method.text.strip() for method in payment_methods_elements]

            price_tag = ad.find_previous('div', class_='headline5')
            if not price_tag:
                continue
            price = price_tag.text.strip()
            price_value = float(price.replace(',', '.'))

            if "Blik" in payment_methods:
                if nickname == "MaxAuto_":
                    maxauto_rate = price_value
                results.append({
                    'nickname': nickname,
                    'payment_methods': payment_methods,
                    'price': price_value
                })
        except Exception as e:
            continue

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n=== Check Time: {current_time} ===")

    if maxauto_rate:
        print(f"MaxAuto_'s rate: {maxauto_rate} PLN")
        better_rates_found = False

        for result in results:
            if result['nickname'] != "MaxAuto_" and result['price'] > maxauto_rate:
                if not better_rates_found:
                    print("\nBetter rates found:")
                    better_rates_found = True
                print(
                    f"Nickname: {result['nickname']}, Payment Methods: {', '.join(result['payment_methods'])}, Exchange Rate: {result['price']} PLN")

        if not better_rates_found:
            print("No better rates found at the moment")
    else:
        print("MaxAuto_ not found in the current listings")


def main():
    print("Starting rate monitoring (Press Ctrl+C to stop)...")

    while True:
        try:
            check_rates()
            time.sleep(60)  # Wait for 1 minute
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)


if __name__ == "__main__":
    main()