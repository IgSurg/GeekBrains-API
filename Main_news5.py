import requests
from lxml import html
from pprint import pprint
from datetime import datetime
import requests
import json
import sys
from pymongo import MongoClient
from sys import platform

if platform == "win32":
    import winsound

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}

#----------------------------------------------------------------------------------------------
"""
Программа для пояска новостей на:
 - news.yandex.ru
 - lenta.ru
 - news.mail.ru
Используется XPATH

И запись в базу Mongodb

"""
#-------------------------------------------------------------------------------------------------




#-------------------------------------------------------------------------------------------------------------------

def get_news_lenta():

    url = 'https://lenta.ru'

    response = requests.get(url, headers=header)
    if response.status_code == 200:
        dom = html.fromstring(response.text)
    else:
        dom = None
    news = []
    try:
        items = dom.xpath("//div[contains(@class,'b-yellow-box__wrap')]/div/a")
    except:
        return news

    cur = str(datetime.now().year)+('.')+str(datetime.now().month)+('.')+str(datetime.now().day)+(' ')+ str(datetime.now().hour)+(':')+ str(datetime.now().minute)
    for item in items:
        new = {}
        text = item.xpath(".//text()")[0]
        source = 'Lenta.ru'
        link = url + item.xpath("@href")[0]
        created_date = cur

        new['text'] = text
        new['source'] = source
        new['link'] = link
        new['created_date'] = created_date

        news.append(new)

    return news

#-------------------------------------------------------------------------------------------------------------------

def get_news_yandex():

    url = 'https://yandex.ru/news'

    response = requests.get(url, headers=header)
    if response.status_code == 200:
        dom = html.fromstring(response.text)
    else:
        dom = None

    news = []
    try:
        items = dom.xpath("//div[contains(@class ,'mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top')]/div")
    except:
        return news


    cur = str(datetime.now().year) + ('.') + str(datetime.now().month) + ('.') + str(datetime.now().day) + (' ')
    for item in items:
        new = {}
        text = '. '.join(item.xpath(".//h2/text()") + item.xpath(".//div[contains(@class,'mg-card__annotation')]/text()"))
        source = ' '.join(item.xpath(".//span[contains(@class,'mg-card-source__source')]/a/text()"))
        link = item.xpath(".//a[contains(@class,'mg-card__link')]/@href")[0]
        created_date = cur + item.xpath(".//span[contains(@class,'mg-card-source__time')]/text()")[0]

        new['text'] = text
        new['source'] = source
        new['link'] = link
        new['created_date'] = created_date

        news.append(new)



    return news
######


#----------------------------------------------------------------------------------------------------------

def get_news_mail_time_source(link):

    url = link

    response = requests.get(url, headers=header)
    if response.status_code == 200:
        dom = html.fromstring(response.text)
    else:
        return None

    try:
        items = dom.xpath("//div[contains(@class,'breadcrumbs_article')]")
    except:
        return None

    try:
        x = items[0].xpath(".//span[contains(@class,'js-ago')]/@datetime")[0]
        y = items[0].xpath(".//a/span[contains(@class,'link__text')]/text()")[0]

    except:
        return None


    return [x, y]

#-----------------------------------------------------------------------------------------------------------

def get_news_mail():

    url = 'https://news.mail.ru/'

    response = requests.get(url, headers=header)
    if response.status_code == 200:
        dom = html.fromstring(response.text)
    else:
        dom = None

    news = []
    try:
        items = dom.xpath("//ul/li[@class='list__item']")
    except:
        return news

#    cur = str(datetime.now().year)+('.')+str(datetime.now().month)+('.')+str(datetime.now().day)+(' ')+ str(datetime.now().hour)+(':')+ str(datetime.now().minute)
    for item in items:
        new = {}
        try:
            text = item.xpath(".//a[@class='list__text']/text()")[0]
            link = item.xpath(".//a[@class='list__text']/@href")[0]
            x = get_news_mail_time_source(link)
            if x is None:
                continue
            else:
                created_date = x[0]
                source = x[1]

            new['text'] = text
            new['source'] = source
            new['link'] = link
            new['created_date'] = created_date
        except:
            continue

        news.append(new)

    return news

#-----------------------------------------------------------------------------------------------------------

def write_to_mongo(ip, port, name_db, news):

    # подключение к базе
    client = MongoClient(ip, port)

    db = client[name_db]
    new = db.news_shelf
# создание уникального индекса

    if 'link_1_source_1' in new.index_information():
        pass
    else:
        res = new.create_index(
       [
        ("link", 1),
        ("source", 1)
        ],unique = True
        )

    # ввод полученного списка вакансий
    count = 0
    for i in range(len(news)):
        try:
            new.insert_one(news[i])
            count += 1
        except:
            pass

    if count > 0:
        print(f"Новых записей {count}")
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 300  # Set Duration To 1000 ms == 1 second
        if platform == "win32":
            winsound.Beep(frequency, duration)
    else:
        print(f"Новых записей нет")

    return count



#-------------------------------------------------------------------------------------------------------------

def main():

#  сбор новостей -----------------------------
    news = get_news_lenta()
    news += get_news_yandex()
    news += get_news_mail()

# запись в базу -----------------------------

    ip = '127.0.0.1'
    port = 27017
    name_db = 'news_aggregation'
    write_to_mongo(ip, port, name_db, news)

# печать результат прохода ------------------
    pprint(news)


#############################################################################################################

if __name__== "__main__":
    main()
