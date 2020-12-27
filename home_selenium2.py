from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
import time
import json
from datetime import datetime
from pymongo import MongoClient
from sys import platform

if platform == "win32":
    import winsound

import requests
import json

# 1
#Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
# в базу данных (от кого, дата отправки, тема письма, текст письма полный)
#Логин тестового ящика: study.ai_172@mail.ru
#Пароль тестового ящика: NextPassword172
#
#--------------------------------------------------------------------------------

def get_mail_text(link, driver):

    try:
        driver.get(link)
    except Exception as e:
        print('фигня какая-то 3:', e)
        return None

    mail = {}
    try:
        m = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'letter__body'))
        )
        mail['text'] = driver.find_element_by_class_name('letter__body').text
        mail['contact'] = driver.find_element_by_class_name('letter-contact').get_attribute('title')
        mail['subject'] = driver.find_element_by_class_name('thread__subject').text
        mail['date'] = driver.find_element_by_class_name('letter__date').text
        mail['date'] = mail['date'].replace('Сегодня,', str(datetime.now().year)+('.')+str(datetime.now().month)+('.')+str(datetime.now().day))
    except Exception as e:
        print('фигня какая-то 4:', e)
        return None


    return mail



#-------------------------------------------------------------------------------------

def register_mailru(link,name,password):

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

    driver.get(link)

    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'email-input'))
        )
        elem = driver.find_element_by_class_name('email-input')
        elem.send_keys(name)
        elem = driver.find_element_by_class_name('button')
        elem.click()
    except Exception as e:
        print('фигня какая-то 1:', e)
        return None

    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'password-input'))
        )
        elem = driver.find_element_by_class_name('password-input')
        elem.send_keys(password)
        elem = driver.find_element_by_class_name('second-button')
        elem.click()
    except Exception as e:
        print('фигня какая-то 2:', e)
        return None

    return driver


#--------------------------------------------------------------------------------------------
def read_mails(driver):

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'js-tooltip-direction_letter-bottom'))
    )

    elems = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
    links = []
    for elem in elems:
         links.append(elem.get_attribute('href'))


    mails = []
    for link in links:
        mail = get_mail_text(link, driver)
        if mail is not None:
            mails.append(mail)

    return mails
#--------------------------------------------------------------------------------------------------------
def read_all_mails(driver):

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'js-tooltip-direction_letter-bottom'))
    )
    count = 0
    end_link = ''
    links = []
    while True:
        time.sleep(3)
        elems = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
        actions = ActionChains(driver)
        actions.move_to_element(elems[-1])
        actions.perform()
        time.sleep(3)

        elems = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')

        for elem in elems:
            try:
                x = elem.get_attribute('href')
            except Exception as e:
                print('фигня какая-то 5:', e)

            links.append(x)
        if x == end_link:
            break
        end_link = x
        count +=1
#        if count > 5: break

    unique_links = list(set(links))    ##  ??????????? дурдом
    mails = []
    for link in unique_links:
        mail = get_mail_text(link, driver)
        if mail is not None:
            mails.append(mail)

    return mails


#-----------------------------------------------------------------------------------------------------------

def write_to_mongo(ip, port, name_db, news):

    # подключение к базе
    client = MongoClient(ip, port)

    db = client[name_db]
    new = db.letters
# создание уникального индекса

    if 'contact_1_date_1_subject_1' in new.index_information():
        pass
    else:
        res = new.create_index(
       [
        ("contact", 1),
        ("date", 1),
        ("subject", 1)
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





#----------------------------------------------------------------------------------------------
def XHR():

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0'}

    url = 'https://e.mail.ru/api/v1/threads/status/smart?folder=0&limit=190&filters=%7B%7D&last_modified=1&force_custom_thread=true&supported_custom_metathreads=%5B%22tomyself%22%5D&offset=0&email=study.ai_172%40mail.ru&htmlencoded=false&token=e221eebc032b88457bf4240becc52b2c%3A474158707754080319510005085654575104000157010f0100015657000005095252525a0c0a5302521654475c6e4206&_=1608843458199'

    response = requests.get(url, headers=header)
    if response.status_code == 200:
        dom = html.fromstring(response.text)
    else:
        dom = None
    return dom

############################################################################################
########################### M - Video ######################################################
############################################################################################
#-----------------------------------------------------------------------------------------------


def get_mvideo_driver(link):
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

    driver.get(link)
    return driver

def get_mvideo_hit_driver(driver):

    try:
        hits = driver.find_elements_by_xpath('//div[@class="section"]')
    except Exception as e:
        print('Хитов нет', e)
        return None
    count = 0
    for hit in hits:
        try:
            dr = hit.find_elements_by_xpath('.//div[contains(text(),"Хиты продаж")]')
            if dr:
                hit_sales = hit
                return hit_sales
            else:
                hit_sales = None
        except Exception as e:
            pass
        count +=1

    return hit_sales

#-----------------------------------------------------------------------------------------------


def get_list_hit_sale(hit_sale):

    items = []

# читаем первую позицию в хитах продаж
    i = 0
    while True:
        try:
            hits = hit_sale.find_elements_by_xpath(".//a[contains(@class,'fl-product-tile-picture fl-product-tile-picture__link')]")
            for hit in hits:
                x = hit.get_attribute('data-product-info')
                x = x.replace('\t', '')
                x = x.replace('\n', '')
                x = json.loads(x)
                x.pop('Location')
                x.pop('eventPosition')
                x.pop('productId')
                x.pop('productCategoryId')
                x.pop('productGroupId')
                if i> 0 and x == items[0]: break
                if x not in items: items.append(x)
                i += 1
        except Exception as e:
            print('фигня какая-то 6:', e)
        if i > 0 and x == items[0]: break

# нажимаем далее

        try:
            button = WebDriverWait(hit_sale, 10).until(
                EC.presence_of_element_located((By.XPATH, './/a[contains(@class,"next-btn")]')))
            button.click()
            time.sleep(2)
        except Exception as e:
            print('фигня какая-то 7:', e)

    return items

#-----------------------------------------------------------------------------------------------

def main():


    link = 'https://mail.ru'
    name = 'study.ai_172@mail.ru'
    password = 'NextPassword172'

    dr = register_mailru(link,name,password)
    if dr is not None:
        mails = read_all_mails(dr)
    pprint(mails)

# запись в базу -----------------------------

    ip = '127.0.0.1'
    port = 27017
    name_db = 'mailru_letters'
    write_to_mongo(ip, port, name_db, mails)

# печать результат прохода ------------------

#    XHR()
##    dr.close()


##########################################################################################################
#Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД. Магазины
#можно выбрать свои. Главный критерий выбора: динамически загружаемые товары


    link = 'https://www.mvideo.ru/'
    dr = get_mvideo_driver(link)
    hit_sale = get_mvideo_hit_driver(dr)
    items = get_list_hit_sale(hit_sale)
    pprint(items)

    dr.close()


# запись в базу -----------------------------

    ip = '127.0.0.1'
    port = 27017
    name_db = 'mvideo'
    write_to_mongo(ip, port, name_db, items)



#############################################################################################################


if __name__== "__main__":
    main()



"""


"""