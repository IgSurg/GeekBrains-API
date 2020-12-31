from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()

driver.get('https://geekbrains.ru/login')


elem = driver.find_element_by_id('user_email')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_id('user_password')
elem.send_keys('Password172')

elem.send_keys(Keys.ENTER)

profile = driver.find_element_by_class_name('avatar')
driver.get(profile.get_attribute('href'))

profile_edit = driver.find_element_by_class_name('text-sm')
driver.get(profile_edit.get_attribute('href'))

gender = driver.find_element_by_name('user[gender]')
select = Select(gender)
select.select_by_value('2')

gender.submit()
driver.close()






