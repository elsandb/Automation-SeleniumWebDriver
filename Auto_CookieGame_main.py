from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import pandas as pd
import datetime as dt

# Settings:
game_length_sec = 20
sec_between_buy = 2
mode = 1  # Mode 1 = 'Buy only one item - the most expensive one. If equal, buy the item furthest down on the list.'
# Todo:     Make other modes. F.eks. When x seconds is passed, spend rest of money on items before ending game.
#           Or buy more than one item each time...
# Todo:     If sec_between_buy = 2, then I will buy the cursor almost every time. This seems to be a good strategy
#           the first 20 sec (at least), but not after a while. Then the cursor becomes more expensive than Grandma.

my_items = {        # List of items that I bought:
    'Cursor': 0,
    'Grandma': 0,
    'Factory': 0,
    'Mine': 0,
    'Shipment': 0,
    'Alchemy lab': 0,
    'Portal': 0,
    'Time machine': 0
}


def money_amount():
    my_money = int(driver.find_element(By.CSS_SELECTOR, 'div#money').text)
    return my_money


def get_price(txt: str):
    a = txt.replace(',', '').split('-')
    item = a[0].strip()
    price_ = int(a[1].strip())
    return item, price_


def buy_something():
    # ----- Check prices in store:
    price_list = []  # --> List [('Cursor', 15), ('Grandma', 100),...]
    store = driver.find_elements_by_css_selector('div#store b')  # Returns 9 elements. I don't want the last one.
    for x in store[0:8]:
        item_price = (get_price(x.text))  # --> tuple of item and price.
        price_list.append(item_price)

    # ----- Check if I will buy/upgrade:
    money = int(driver.find_element(By.CSS_SELECTOR, 'div#money').text)
    buy_price = 0
    buy_item = ""
    buy_index = ""

    for tup in price_list:
        item_price = tup[1]
        if money >= item_price >= buy_price:
            buy_price = item_price
            buy_item = tup[0]
            buy_index = price_list.index(tup)

    # Buy something:
    id_list = ['buyCursor', 'buyGrandma', 'buyFactory', 'buyMine', 'buyShipment',
               'buyAlchemy lab', 'buyPortal', 'buyTime machine']
    if buy_price > 0:
        driver.find_element(By.ID, f'{id_list[buy_index]}').click()
        my_items[f"{buy_item}"] += 1


# Get website:
driver = webdriver.Chrome(executable_path='C:/Development/chromedriver.exe')
driver.get('http://orteil.dashnet.org/experiments/cookie/')

# Wait for cookie-question popup, then click on the 'got it'-button:
wait = WebDriverWait(driver, 10)
got_it_button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'a.cc_btn')))
got_it_button.click()

# Play game
game_on = True
t0 = time.time()
t1 = time.time()

while game_on:
    if time.time() >= t0 + game_length_sec:
        game_on = False
    driver.find_element(By.ID, 'cookie').click()
    if time.time() >= t1 + sec_between_buy:
        buy_something()
        t1 = time.time()


# ----- STATISTICS ----- #
game = {
    'game_id': dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
    'game_length': game_length_sec,
    'sec_between_buy': sec_between_buy,
    'mode': mode,
    'cps': float(driver.find_element(By.ID, 'cps').text.split(' : ')[1]),
    'money': int(driver.find_element(By.CSS_SELECTOR, 'div#money').text),
}
game_stats = {**game, **my_items}
game_stats_df = pd.DataFrame(game_stats, index=[0])

# Add new row with stats for this game to csv file:
game_stats_df.to_csv('game_stats.csv', mode='a', index_label=False, index=False, header=False)

# Print stats
all_stats = pd.read_csv('game_stats.csv')
print(all_stats.to_string())
