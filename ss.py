import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


link = 'https://yandex.com/web-maps/2/saint-petersburg/?ll=30.283493%2C59.925669&mode=poi&poi%5Bpoint%5D=30.283824%2C59.927957&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D1053830005&tab=reviews&utm_source=review&z=16'

with webdriver.Chrome() as browser:
    browser.get(link)
    for i in range(2):
        time.sleep(3)
        div = browser.find_element(By.CSS_SELECTOR, 'div.card-reviews-view')
        div.click().send_keys(Keys.END)

        ActionChains(browser).click(div).send_keys(Keys.END).perform()
        # scrollbar.send_keys(Keys.END)
        time.sleep(3)