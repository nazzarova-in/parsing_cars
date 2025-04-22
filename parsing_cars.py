from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import json

from sort_cars import find_prices
#
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# service = Service('D:/chromedriver-win32/chromedriver.exe')
# driver = webdriver.Chrome(service=service, options=chrome_options)

CAR_SELECTOR = "div.AdPhoto_wrapper__gAOIH"
TITLE_SELECTOR = "a.AdPhoto_info__link__OwhY6"
PRICE_SELECTOR = "span.AdPrice_price__2L3eA"
PAGINATION_SELECTOR = "button.Pagination_pagination__container__buttons__wrapper__icon__next__A22Rc"

OUTPUT_FILE = "prices.json"
BASE_URL = "https://999.md/ru/list/transport/cars?appl=1&ef=16%2C1%2C6%2C2200&o_1_2095_8_98=36187"

all_cars = []

def write_data_json(data):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parsing_cars():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service('D:/chromedriver-win32/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        page = 1
        while True:
            if page == 1:
                url = BASE_URL
            else:
                url = f"{BASE_URL}&page={page}"

            print(f"Обрабатывается страница {page}...")
            driver.get(url)
            time.sleep(2)

            cars_on_page = 0
            for car in driver.find_elements(By.CSS_SELECTOR, CAR_SELECTOR[3:]):
                try:
                    title_elem = car.find_element(By.CSS_SELECTOR, TITLE_SELECTOR)
                    title = title_elem.text
                    link = title_elem.get_attribute('href')
                    price = car.find_element(By.CSS_SELECTOR, PRICE_SELECTOR).text

                    if title and price:
                        original_title = title
                        split_string = original_title.split(',')

                        title = split_string[0]
                        year = split_string[1].strip() if len(split_string) > 1 else None

                        if title == 'Renault Megane' and year == '2007 г.':
                            all_cars.append({
                                "title": title,
                                "year": year,
                                "price": price,
                                "link": link,
                            })
                        cars_on_page += 1


                except NoSuchElementException:
                    continue

            print(f"Страница {page}: найдено {cars_on_page} авто")

            try:
                next_btn = driver.find_element(By.CSS_SELECTOR, PAGINATION_SELECTOR)
                if next_btn.get_attribute("disabled"):
                    break

                page += 1
            except NoSuchElementException:
                break

    finally:
        driver.quit()

        result = find_prices(all_cars)

        write_data_json(result)

