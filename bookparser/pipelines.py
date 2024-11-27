# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class BookparserPipeline:
    def __init__(self):
        # Настраиваем клиент MongoDB (IP, порт)
        client = MongoClient('localhost', 27017)
        # Задаём название базы данных
        self.mongo_base = client.books_labirint


    def process_item(self, item, spider):
        # коллекция в БД (имя паука)
        collection = self.mongo_base[spider.name]

        # id
        try:
            *_, id, _ = item['link'].split('/')
            item['_id'] = id
        except ValueError:
            item['_id'] = None

        # название
        _, title = item.get('title').split(':')
        item['title'] = title.strip()

        # авторы
        item['author'] = ', '.join(item['author'])

        # художники
        item['artist'] = ', '.join(item['artist'])

        # переводчики
        item['translator'] = ', '.join(item['translator'])

        # редакторы
        item['editor'] = ', '.join(item['editor'])

        # издательство
        item['publishing'] = ', '.join(item['publishing'])

        # год издания книги
        try:
            year = re.sub(r'\D', '', item['year'][1])
            item['year'] = int(year)
        except ValueError:
            item['year'] = None

        # серия
        item['series'] = ', '.join(item['series'])

        # коллекция
        item['collection'] = ', '.join(item['collection'])

        # жанр
        item['genre'] = ', '.join(item['genre'])

        # масса книги
        try:
            weight = re.sub(r'\D', '', item['weight'])
            item['weight'] = int(weight)
        except ValueError:
            item['weight'] = None

        # размеры книги
        try:
            *_, dimensions, _ = item['dimensions'].split(' ')
            length, width, height = dimensions.split('x')
            item['dimensions'] = {'length': int(length), 'width': int(width), 'height': int(height)}
        except ValueError:
            item['dimensions'] = {'length': None, 'width': None, 'height': None}

        # рейтинг
        try:
            item['rating'] = float(item['rating'])
        except ValueError:
            item['rating'] = None

        # цена
        try:
            item['price'] = float(item['price'])
        except ValueError:
            item['price'] = None

        try:
            # Добавляем запись в базу данных
            collection.insert_one(item)
        except ValueError:
            print('Ошибка добавления документа')

        return item
