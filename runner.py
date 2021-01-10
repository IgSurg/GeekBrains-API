from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroy_merlin.spiders.leroyspider import LeroyTheSpiderSpider

from leroy_merlin import settings

if __name__ == '__main__':  #

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    search = 'зеркало'
    search2 = 'ковер'
    search3 = 'люстры'
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyTheSpiderSpider, search,search2,search3)


    process.start()


