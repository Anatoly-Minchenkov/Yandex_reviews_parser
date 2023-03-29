import time


from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By

def more_button_checker(rewiew, browser, scrollbar):
    if len(rewiew.find_elements(By.CSS_SELECTOR, '.business-review-view__expand')) != 0:
        more_button = rewiew.find_element(By.CSS_SELECTOR, '.business-review-view__expand')
        ActionChains(browser).move_to_element(more_button).click_and_hold(scrollbar).move_by_offset(0, 10).release().perform()
        more_button.click()


def screenshoot_maker(browser, rewiew, scrollbar, count):
    # ActionChains(browser).move_to_element(rewiew).perform()
    # ActionChains(browser).click_and_hold(scrollbar).move_by_offset(0, 5).release().perform()
    # more_button_checker(rewiew, browser, scrollbar)

    print(f"Сделан скриншот {count}")

def comment_founder(link, comment, headless=True, screenshot=True):
    if headless:
        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument('--headless')
    else:
        options_chrome = webdriver.ChromeOptions()

    with webdriver.Chrome(options=options_chrome) as browser:
        browser.get(link)
        time.sleep(3) #надо сделать ожидания
        review_count = browser.find_element(By.CSS_SELECTOR, 'span[itemprop="aggregateRating"] meta[itemprop=reviewCount]').get_attribute('content')
        rating = browser.find_element(By.CSS_SELECTOR, 'span[itemprop="aggregateRating"] meta[itemprop=ratingValue]').get_attribute('content')
        all_review = browser.find_elements(By.CLASS_NAME, 'business-reviews-card-view__review')
        scrollbar = browser.find_element(By.CSS_SELECTOR, 'div.scroll__scrollbar-thumb')

        for count, rewiew in enumerate(all_review, start=1):
            rewiew_text = rewiew.find_element(By.CSS_SELECTOR, '.business-review-view__body-text').text
            # if comment in rewiew_text:
            print('Отзыв найден')
            if screenshot:
                rewiew.screenshot(f"screen/screen{count}.png")
                print('Скриншот сделан')
        else:
            print('Отзыв не найден')
        print(f'Всего отзывов - {review_count}\n'
              f'Рейтинг - {rating}')


link = 'https://yandex.com/maps/2/saint-petersburg/?ll=30.288464%2C59.924127&mode=poi&poi%5Bpoint%5D=30.283425%2C59.925505&poi%5Buri%5D=ymapsbm1%3A%2F%2Forg%3Foid%3D1069493507&tab=reviews&z=16'
comment = 'Максимально простая обстановка и в то же время очень душевная атмосфера'
comment_founder(link, comment)