# Yandex_reviews_parser

На одном из моих недавних фриланс-проектов была поставлена задача реализовать парсер, проверяющий наличие/отсутствие отзыва на Яндек.Картах. 
Задача была успешна выполнена, и сейчас, спустя время, я решил поделиться этой частью данного проекта, немного расшириф его функциональность.

#

### :bookmark_tabs: Использование
Программа имеет два класса, которые отвечают за разный функционал:
- **Yandex_reviews_parser(link, headless=True, screenshots=False)** - Парсит и записывает данные об отзыве в таблицу Exel;
  -  link - Принимает ссылку на страницу c отзывами на яндекс.картах
  -  headless - Принимает True/False. Определяет, нужно ли запускать браузер в фоновом режиме
  -  screenshots - Принимает True/False.  Определяет, нужно ли делать скриншоты спаршенных комментариев
- **Search_comment_in_reviews(link, review_to_check, headless=True, screenshots=True)** - Проверяет наличие переданного в неё отзыва, среди всех размещенных отзывов на странице.
  - link, headless, screenshots - Принимают такие-же значения, как и Yandex_reviews_parser
  - review_to_check - Принимает отзыв, который нужно найти

**Результат:**

В папке exel_files появится exel-файл, имеющий название объекта парсинга, и содержащий информацию об отзывах.

В папке screens будут сохранены скриншоты отзывов

### :hammer_and_wrench: Установка:
1. $ pip install -r requirements.txt
2. Необходимо наличие ChromeDriver для selenium (https://chromedriver.chromium.org/downloads)
