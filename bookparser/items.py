# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class BookparserItem(scrapy.Item):
    title = scrapy.Field()  # название
    author = scrapy.Field()  # автор
    artist = scrapy.Field()  # художник
    translator = scrapy.Field()  # переводчик
    editor = scrapy.Field()  # редактор
    publishing = scrapy.Field()  # издательство
    year = scrapy.Field()  # год
    series = scrapy.Field()  # серия
    collection = scrapy.Field()  # коллекция
    genre = scrapy.Field()  # жанр
    weight = scrapy.Field()  # масса
    dimensions = scrapy.Field()  # размеры
    price = scrapy.Field()  # цена
    rating = scrapy.Field()  # рейтинг
    link = scrapy.Field()  # url
    _id = scrapy.Field()  # id в базе данных
