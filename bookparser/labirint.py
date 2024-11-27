import scrapy
from scrapy.http import HtmlResponse
from S05.bookparser.items import BookparserItem

class LabirintSpider(scrapy.Spider):
    name = "labirint"   # имя паука
    allowed_domains = ["labirint.ru"]    # список разрешенных доменов
    start_urls = ["https://www.labirint.ru/genres/3079/"]    # точка входа


    # метод парсит основные страницы
    def parse(self, response:HtmlResponse):
        # Получаем ссылку на следующую страницу, если она есть
        next_page = response.xpath("//div[@class = 'pagination-next']/a/@href").get()
        if next_page:
            # рекурсивный вызов функции со ссылкой на следующую страницу
            yield response.follow(next_page, callback=self.parse)

        # Собираем ссылки со всех книг на странице
        links = response.xpath("//div[contains(@class,'catalog-responsive')]//a[@class='product-title-link']/@href").getall()
        for link in links:
            # Делаем запросы для каждой ссылке, ответы от запросов будут направлятся в метод book_parse
            yield response.follow(link, callback=self.book_parse)


    # метод парсит страницы с описанием
    def book_parse(self, response:HtmlResponse):
        title = response.xpath("//h1/text()").get()  # название

        description = response.xpath("//div[@class='product-description']")
        author = description.xpath(".//a[@data-event-label='author']/text()").getall()   # автор
        artist = description.xpath("./div[@class='authors']/a[not(@data-event-label)]/text()").getall()   # художник
        translator = description.xpath(".//a[@data-event-label='translator']/text()").getall()  # переводчик
        editor = description.xpath(".//a[@data-event-label='editor']/text()").getall()   # редактор
        publishing = description.xpath(".//a[@data-event-label='publisher']/text()").getall()   # издательство
        year = description.xpath(".//div[@class='publisher']/text()").getall()   # год
        series = description.xpath(".//a[@data-event-label='series']/text()").getall()   # серия
        collection = description.xpath(".//div[@class='collections']/a/text()").getall()   # коллекция
        genre = description.xpath(".//a[@data-event-label='genre']/text()").getall()   # жанр
        weight = description.xpath(".//div[@class='weight']/text()").get()   # масса
        dimensions = description.xpath(".//div[@class='dimensions']/text()").get()   # размеры
        price = description.xpath(".//span[@class='buying-pricenew-val-number']/text()").get()   # цена

        rating = response.xpath("//div[@id='rate']/text()").get()   # рейтинг
        link = response.url   # url

        # Отправляем данные в Pipeline
        yield BookparserItem(title=title,
                             author=author,
                             artist=artist,
                             translator=translator,
                             editor=editor,
                             publishing=publishing,
                             year=year,
                             series=series,
                             collection=collection,
                             genre=genre,
                             weight=weight,
                             dimensions=dimensions,
                             price=price,
                             rating=rating,
                             link=link)





