import os
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def make_screenshot(review, platform_name):
    comment_date = review.find_element(By.CSS_SELECTOR, '.business-review-view__date meta').get_attribute('content')\
        .split('.')[0].replace(':', '-')
    review.screenshot(f"screen/{platform_name}{comment_date}.png")
    print(f'Скриншот {platform_name}{comment_date}.png сделан')

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

def load_new_50_comments(browser, list_review):
    actual_len = len(list_review)
    div = browser.find_element(By.CSS_SELECTOR, 'div.card-reviews-view')
    ActionChains(browser).click(div).send_keys(Keys.END).send_keys(Keys.PAGE_UP).perform()
    try:
        WebDriverWait(browser, 5, poll_frequency=0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.business-reviews-card-view__review:nth-child({actual_len+2})'))) # яндекс подгружает до nth51
    except:
        return
def yandex_comment_searcher(link, comment, headless=False):
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless') if headless else None

    with webdriver.Chrome(options=options_chrome) as browser:
        list_review = []
        browser.get(link)
        WebDriverWait(browser, 10, poll_frequency=0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.business-review-view')))
        review_count = browser.find_element(By.CSS_SELECTOR, 'span[itemprop="aggregateRating"] meta[itemprop=reviewCount]').get_attribute('content')
        rating = browser.find_element(By.CSS_SELECTOR, 'span[itemprop="aggregateRating"] meta[itemprop=ratingValue]').get_attribute('content')

        for _ in range(int(review_count)//50 + 1):
            if comment_in_50_comments(browser, comment, list_review):
                break
            else:
                    load_new_50_comments(browser, list_review)
        else:
            print('Не опубликован')
        print(f'Всего отзывов - {review_count}\nРейтинг - {rating}\nКоличество скриншотов - {len(os.listdir("screen"))}')


link = 'https://yandex.com/web-maps/2/saint-petersburg/?ll=30.286638%2C59.923294&mode=poi&poi%5Bpoint%5D=30.277649%2C59.924625&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D1194959046&tab=reviews&utm_source=review&z=15.65'
comment = 'Ребята стараются, это видно. Есть увлечённые делом парни. Осталась некоторая'
yandex_comment_searcher(link, comment)
