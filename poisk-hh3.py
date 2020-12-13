from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
import sys

#
# Поиск вакансий на hh.ru, название вакансии для поиска в переменной vacancy_find
# Результат - список
# {'employer': ' название',
#   'employer_link': 'линк на заказчика',
#   'link': 'линк на вакансию',
#   'name': 'название вакансии',
#   'salary': 'зарплата'}
#


def salary_define(salary):
    ret = [None,None,None]
    salary = salary.replace(u'\xa0', u' ')
    salary = salary.lower()
    if salary.lower().find('до') >= 0:
        s = salary[salary.lower().find('до')+2:]
        if s.find('руб') >= 0:
            s = s[0:s.find('руб')]
            ret[1] = int(s.replace(' ',''))
            ret[2] = 'РУБ'
        elif s.find('usd') >= 0:
            s = s[0:s.find('usd')]
            ret[1] = int(s.replace(' ',''))
            ret[2] = 'USD'
        else:
            pass
    elif salary.lower().find('от') >= 0:
        s = salary[salary.lower().find('от')+2:]
        if s.find('руб') >= 0:
            s = s[0:s.find('руб')]
            ret[1] = int(s.replace(' ',''))
            ret[2] = 'РУБ'
        elif s.find('usd') >= 0:
            s = s[0:s.find('usd')]
            ret[1] = int(s.replace(' ',''))
            ret[2] = 'USD'
        else:
            pass
    elif salary.lower().find('-') >= 0:
        s = salary.lower()
        if s.find('руб') >= 0:
            s = s[0:s.find('руб')]
            x = s.split("-")
            ret[0] = int(x[0].replace(' ',''))
            ret[1] = int(x[1].replace(' ', ''))
            ret[2] = 'РУБ'
        elif s.find('usd') >= 0:
            s = s[0:s.find('usd')]
            ret[0] = int(x[0].replace(' ', ''))
            ret[1] = int(x[1].replace(' ', ''))
            ret[2] = 'USD'
        else:
            pass
    else:
        pass
    return ret


# -------------------------------------------------------------------------------------

main_link = 'https://hh.ru'
vacancy_find = 'data-analyst'
link = f'{main_link}/vacancies/{vacancy_find}'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

vacancy_list = []

while True:
    response = requests.get(link, headers=headers)
    if response.ok:
        soup = bs(response.text, 'html.parser')
    else:
        break
    vacs = soup.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})

    for vac in vacs:
        vac_data = {}
#  название вакансии
        vac_name = vac.find('a')
        vac_data['name'] = vac_name.text
#        vac_data['name'] = vac_name.text.decode('utf-8')

#  зарплата вакансии
        try:
            vac_salary = vac.find('span',{'data-qa':'vacancy-serp__vacancy-compensation'})
            salary_def = salary_define(vac_salary.text)
            vac_data['MIN salary'] = salary_def[0]
            vac_data['MAX salary'] = salary_def[1]
            vac_data['CUR salary'] = salary_def[2]
        except:
            vac_data['MIN salary'] = None
            vac_data['MAX salary'] = None
            vac_data['CUR salary'] = None
        #  link вакансии
        try:
            vac_data['link'] = str(vac.find('a')['href'])
        except:
            vac_data['link'] = ''
#  компания вакансии
        try:
            vac_emp = vac.find('div', {'class': 'vacancy-serp-item__meta-info-company'})
            vac_employer = vac_emp.find('a')
            vac_data['employer'] = vac_employer.text
        except:
            vac_data['employer'] = ''
#  линк компания вакансии
        try:
            vac_emp = vac.find('div', {'class': 'vacancy-serp-item__meta-info-company'})
            vac_employer_link = vac_emp.find('a')['href']
            vac_data['employer_link'] = main_link + vac_employer_link
        except:
            vac_data['employer_link'] = ''

        vacancy_list.append(vac_data)

#  переход на следующую страницу вакансии
    try:
        next =  soup.find('a',{'class':'HH-Pager-Controls-Next'})
        if next.text == 'дальше':
            link = main_link + next['href']
        else:
            break
    except:
        break

#-------------------------------------------------------------------------------------------


print('Количество ', len(vacancy_list))
pprint(vacancy_list)

# write to file
with open("hh vacancy.json", "w") as f:
    json.dump(vacancy_list, f)

pass



#######################################################################################
