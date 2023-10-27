from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import time
from mynewsapp.models import NewsArticle
from datetime import datetime
import requests

class Command(BaseCommand):
    help = 'Your custom command description here'

    def handle(self, *args, **options):
        user_keyword = input("Введите ключевое слово для поиска новостей: ")
        while True:
            self.get_and_save_news(user_keyword)
            self.stdout.write(self.style.SUCCESS('Новости успешно добавлены в базу данных.'))
            time.sleep(600)  # Подождать 10 минут перед следующим запросом

    def parse_date(self, date_string):
        hours, minutes = map(int, date_string.split(':'))
        current_date = datetime.now().date()
        parsed_date = datetime(current_date.year, current_date.month, current_date.day, hours, minutes)
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return formatted_date

    def get_and_save_news(self, keyword):
        url = 'https://ria.ru/world/'
        response = requests.get(url)

        news_list = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            titles = soup.find_all(class_='list-item__title')
            dates = soup.find_all(class_='list-item__date')

            for title, date in zip(titles, dates):
                article_title = title.text.strip()
                article_link = title['href']
                publication_time = self.parse_date(date.text.strip())

                if keyword in article_title:
                    news_list.append({'title': article_title, 'link': article_link, 'time': publication_time})
                    news_article = NewsArticle(
                        publication_date=publication_time,
                        title=article_title,
                        news_link=article_link
                    )
                    news_article.save()





