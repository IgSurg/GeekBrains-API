from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru')

try:
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'email-input'))
    )
    elem = driver.find_element_by_class_name('email-input')
    elem.send_keys('study.ai_172@mail.ru')
    elem = driver.find_element_by_class_name('button')
    elem.click()
except Exception as e:
    print('Сбор закончен или ошибка:', e)

elem = driver.find_element_by_class_name('password-input')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)

time.sleep(5)
elems = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
link = []
for elem in elems:
     link.append(elem.get_attribute('href'))

pass



"""


"""