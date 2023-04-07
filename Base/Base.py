import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By


class Base_class:
    '''Базовый класс, который содержит многократно-используемые функции
           -link - принимает ссылку на страницу с отзывами на яндекс.картах
           -comment - Принимает комментарий, который нужно найти
           -headless - Принимает True/False. Определяет, нужно ли отображать браузер
           -screenshots - Принимает True/False.  Определяет, нужно ли делать скриншоты спаршенных комментариев
    '''

    def __init__(self, link, headless=True, screenshots=False):
        self.link = link
        # self.comment = comment
        self.headless = headless
        self.screenshots = screenshots
        self.set_review = set()
        self.reviews_count = 0
        self.options_chrome = webdriver.ChromeOptions()
        self.options_chrome.add_argument('--headless') if self.headless else None
        self.browser = webdriver.Chrome(options=self.options_chrome)
        self.browser.get(self.link)
        self.review_count, self.location_name = self.get_variables()

        if self.screenshots:
            if not os.path.isdir(f'screen/{self.location_name}'):
                os.mkdir(f'screen/{self.location_name}')

    def __del__(self):
        '''функция-финализатор'''
        self.browser.close()

    def get_variables(self):
        '''До старта парсинга отзывов, функция парсит необходимые переменные'''
        self.wait_elem(By.CSS_SELECTOR, 'div.business-review-view')
        review_count = self.browser.find_element(By.CSS_SELECTOR,'span[itemprop="aggregateRating"] meta[itemprop=reviewCount]').get_attribute('content')
        location_name = self.browser.find_element(By.CSS_SELECTOR,'div .card-title-view__title').text
        return (review_count, location_name)

    def wait_elem(self, selector, locator):
        WebDriverWait(self.browser, 10, poll_frequency=0.5).until(EC.presence_of_element_located((f'{selector}', f'{locator}')))

    def make_screenshot(self, review):
        '''Функия создания скриншота'''
        name = str(self.reviews_count) + '_' + review.find_element(By.CSS_SELECTOR, '.business-review-view__author span').text.strip(':?<>|*\\/.')
        filename = f"screen/{self.location_name}/{name}.png"
        review.screenshot(f"{filename}")
        print(f'Скриншот {name}.png сделан')

    def load_new_50_reviews_on_page(self):
        '''Функия подргузки комментариев (Yandex подгружает по 50 комментариев за раз)'''
        actual_len = len(self.set_review)
        div = self.browser.find_element(By.CSS_SELECTOR, 'div.card-reviews-view')
        ActionChains(self.browser).click(div).send_keys(Keys.END).send_keys(Keys.PAGE_UP).perform()
        try:
            WebDriverWait(self.browser, 8, poll_frequency=0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'div.business-reviews-card-view__review:nth-child({actual_len + 2})')))  # яндекс подгружает до nth51
        except:
            return


