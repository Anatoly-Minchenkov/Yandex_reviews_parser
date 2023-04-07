from Base.Base import Base_class

import openpyxl
from selenium.webdriver.common.by import By


class Yandex_reviews_parser(Base_class):
    '''Класс парсинга и записи данных в exel
       -link - ссылка на страницу яндекс.карт
       -headless - Принимает True/False. Определяет, нужно ли запускать браузер в фоновом режиме
       -screenshots - Принимает True/False.  Определяет, нужно ли делать скриншоты спаршенных отзывов
    '''

    def __init__(self, link, headless=True, screenshots=False):
        super().__init__(link, headless, screenshots)
        self.create_exel_file()
        self.exel_reviews_adder()

    def create_exel_file(self):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Дата размещения', 'Оценка', 'Имя', 'Отзыв'])
        workbook.save(f'exel_files/{self.location_name}.xlsx')

    def connect_to_exel_file(self):
        self.workbook = openpyxl.load_workbook(f'exel_files/{self.location_name}.xlsx')
        self.sheet = self.workbook.active

    def exel_reviews_adder(self):
        '''Реализация логики записи отзывов в exel'''
        self.wait_elem(By.CSS_SELECTOR, 'div.business-review-view')
        for _ in range(int(self.review_count) // 50 + 1):
            self.connect_to_exel_file()
            self.add_50_reviews_to_exel()
            self.load_new_50_reviews_on_page()
            self.workbook.save(f'exel_files/{self.location_name}.xlsx')
            print(f'Добавлено записей: {self.reviews_count}')
        print('Все отзывы сохранены')

    def add_50_reviews_to_exel(self):
        '''Функция парсит новоподгруженные отзывы'''
        all_review = self.browser.find_elements(By.CSS_SELECTOR, 'div.business-review-view')
        for review in all_review:
            if review not in self.set_review:
                self.set_review.add(review)
                self.reviews_count += 1
                self.add_review_to_exel(review)
                if self.screenshots:
                    self.make_screenshot(review)
        return False

    def add_review_to_exel(self, review):
        '''Функция добавляет в exel строку спаршенных данных'''
        date = review.find_element(By.CSS_SELECTOR, '.business-review-view__date meta').get_attribute('content').split('T')[0]
        ismark = len(review.find_elements(By.CSS_SELECTOR, '[itemprop="reviewRating"] [itemprop="ratingValue"]'))
        mark = review.find_element(By.CSS_SELECTOR, '[itemprop="reviewRating"] [itemprop="ratingValue"]').get_attribute('content')[0] if ismark else '-'
        name = review.find_element(By.CSS_SELECTOR, '.business-review-view__author span').text
        review_text = review.find_element(By.CSS_SELECTOR, 'span.business-review-view__body-text').text
        self.sheet.append([date, mark, name, review_text])

class Search_review_in_reviews(Base_class):
    '''Класс поиска наличий переданного отзыва среди всех отзывов
       -link - принимает ссылку на страницу с отзывами на яндекс.картах
       -review_to_check - Принимает отзыв, который нужно найти
       -headless - Принимает True/False. Определяет, нужно ли запускать браузер в фоновом режиме
       -screenshots - Принимает True/False.  Определяет, нужно ли делать скриншоты спаршенных отзывов
    '''

    def __init__(self, link, review_to_check, headless=True, screenshots=True):
        super().__init__(link, headless, screenshots)
        self.review_to_check = review_to_check
        self.yandex_review_searcher()
        # print(self.__dict__)

    def yandex_review_searcher(self):
        '''Реализация логики посика отзыва'''
        self.wait_elem(By.CSS_SELECTOR, 'div.business-review-view')
        for _ in range(int(self.review_count) // 50 + 1):
            if self.find_review_in_50_reviews():
                break
            else:
                self.load_new_50_reviews_on_page()
        else:
            print('Такого отзыва нет')

    def find_review_in_50_reviews(self):
        '''Функиця ищет переданный отзыв'''
        all_review = self.browser.find_elements(By.CSS_SELECTOR, 'div.business-review-view')
        for review in all_review:
            if review not in self.set_review:
                self.set_review.add(review)
                review_text = review.find_element(By.CSS_SELECTOR, 'span.business-review-view__body-text').text
                if self.review_to_check in review_text:
                    print('Отзыв размещен')
                    if self.screenshots:
                        self.reviews_count += 1
                        self.make_screenshot(review)
                    return True
        return False


link = 'https://yandex.com/maps/org/triumfalna_arka_holovnoho_shtabu/170068743929/reviews/?display-text=%D0%94%D0%BE%D1%81%D1%82%D0%BE%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%87%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C&ll=30.318384%2C59.937857&mode=search&sctx=ZAAAAAgBEAAaKAoSCQpMp3UbVD5AEZt1xvfF901AEhIJMnGrIAa6wj8RNpNvtrkxpT8iBgABAgMEBSgKOABA5a4HSAFqAnVhnQHNzEw9oAEAqAEAvQFjOhZEwgGRAdLpzrjWBf2D%2FMPWAtDF9OTfAubXxIq2A%2BC68KPOA5yTzv6ZA46W3%2FGUBOyp39DvAvmTlr0dn9zmlqIG0av2npIE2JWu%2BAOYn%2F2OUr2S9PEDuqi1guwE0dWP8%2BsDpIGfgAXdzNGVjQb5rYzH%2BQSn7bmLtgPMz5ey%2BQSv4cnGnQLYlL%2FhtQP43YeVlQSal5m7%2BQTqAQDyAQD4AQCCAh0oKGNhdGVnb3J5X2lkOig4OTY4MzM2ODUwOCkpKYoCCzg5NjgzMzY4NTA4kgIAmgIMZGVza3RvcC1tYXBz&sll=30.318384%2C59.937857&sspn=0.009611%2C0.004728&tab=reviews&text=%7B%22text%22%3A%22%D0%94%D0%BE%D1%81%D1%82%D0%BE%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%87%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C%22%2C%22what%22%3A%5B%7B%22attr_name%22%3A%22category_id%22%2C%22attr_values%22%3A%5B%2289683368508%22%5D%7D%5D%7D&z=16.33'
# Yandex_reviews_parser(link, headless=True, screenshots=False)

### Поиск переданного отзыва, и создание его скриншота ###
review_to_check = '''Сердце спб, красота и величие.'''
Search_review_in_reviews(link, review_to_check, headless=True, screenshots=True)
