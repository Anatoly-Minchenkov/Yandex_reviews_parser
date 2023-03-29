import os
import time
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def make_screenshot(review, platform):
    comment_date = review.find_element(By.CSS_SELECTOR, '.business-review-view__date meta').get_attribute('content')\
        .split('.')[0].replace(':', '-')
    review.screenshot(f"screen/{platform}{comment_date}.png")
    print(f'Скриншот {platform}{comment_date}.png сделан')

def comment_in_50_comments(browser,comment, list_review):
    all_review = browser.find_elements(By.CSS_SELECTOR, 'div.business-review-view')
    for review in all_review:
        if review not in list_review:
            list_review.append(review)
            review_text = review.find_element(By.CSS_SELECTOR, 'span.business-review-view__body-text').text
            if comment in review_text:
                print('Размещен')
                make_screenshot(review, 'yandex')
                return True


def yandex_comment_found(link, comment, headless=True):
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless') if headless else None

    with webdriver.Chrome(options=options_chrome) as browser:
        list_review = []
        browser.get(link)
        WebDriverWait(browser, 10, poll_frequency=0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.business-review-view')))
        review_count = browser.find_element(By.CSS_SELECTOR, 'span[itemprop="aggregateRating"] meta[itemprop=reviewCount]').get_attribute('content')
        rating = browser.find_element(By.CSS_SELECTOR, 'span[itemprop="aggregateRating"] meta[itemprop=ratingValue]').get_attribute('content')

        for _ in range(int(review_count)//50):
            if comment_in_50_comments(browser, comment, list_review):
                break
            else:
                pass
        else:
            print('Не опубликован')
        print(f'Всего отзывов - {review_count}\nРейтинг - {rating}\nКоличество скриншотов - {len(os.listdir("screen"))}')


link = 'https://yandex.com/web-maps/2/saint-petersburg/?ll=30.283493%2C59.925669&mode=poi&poi%5Bpoint%5D=30.283824%2C59.927957&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D1053830005&tab=reviews&utm_source=review&z=16'
comment = 'Очень прнрааилрсь'
yandex_comment_found(link, comment)
