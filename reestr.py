#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup
import requests
requests.packages.urllib3.disable_warnings()
import urllib.request
import ssl
import re
months = {'Января':'01', 'Февраля':'02','Марта':'03','Апреля':'04','Мая':'05','Июня':'06','Июля':'07',
          'Августа':'08','Сентября':'09','Октября':'10','Ноября':'11','Декабря':'11'}
import time


# In[ ]:





# In[2]:


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

baseurl = 'https://reestr.digital.gov.ru'


# In[3]:


#поиск количества страниц c отображением по 100
def find_n():
    req = requests.get('https://reestr.digital.gov.ru/reestr/?show_count=100', verify=False).text
    res = BeautifulSoup(req, 'lxml').find('div', class_='page_nav_area').find_all('a', class_='nav_item')
    return int(res[3].text)+1


# In[8]:


print('Создание ссылок для всех страниц поиска на сайте реестра (с отображением по 100)')
with open('links.txt', mode='w', encoding='utf-8') as myfile:
    for i in range(1, find_n()):
    # Создание ссылок для всех страниц поиска на сайте реестра (с отображением по 100)
        url = baseurl + '/reestr/?PAGEN_1=' + str(i) + '&show_count=100'
        response = urllib.request.urlopen(url)
        print(url)
        # поиск ссылок на страницы с юридической информации о ПО
        links = re.findall('<a href=\"(/reestr/\d*/)\"', str(response.read()))
        for line in links:
            print(baseurl + line, file=myfile)


# In[4]:


# константные значения
links = "links.txt"
# количество уникальных названий ПО
f = open(links)
content = f.readlines()
num = len(content)
print(f'Всего ссылок: {num} \n введите номер ссылки, с которой начать парсинг(включительно):')
try:
    num0 = int(input()) - 1
except:
    print('введите целое число!')
print('введите номер ссылки, на которой закончить парсинг(включительно):')
try:
    num1 = int(input())
except:
    print('введите целое число!')
num = num1 - num0
print(f'Будет распарсено {num} ссылок. Введите название файла:')
try:
    filename = input()
except:
    print('введите корректное название')
print('Будем делать паузы после n ссылок? y/n')
if input()=='y':
    print('после скольки ссылок делать паузы?')
    frame = int(input())
    print('сколько секунд будут длится паузы?')
    seconds = int(input())
else:
    frame = 1000
    seconds = 0
print('ну и последний вопрос: какой формат выходного файла желаете? 1 - xlsx, 2 - csv, 3 - оба')
try:
    format_ = int(input())
except:
    print('введите целое число (1, 2, 3) без посторонних символов и пробелов!')
    
# создание словаря для передачи его в последствии датафрейму в пандас
values = {'Название по': [], 'Ссылка на ПО':[], 'Вид организации':[],'Название организации': [], 'Все продукты организации':[], 
          'ИНН': [],'Сведения об исключительном праве':[],'Альтернатив': [], 'Класс по': [],  'Сайт': [], 'Дата регистрации':[], 'Рег.номер ПО':[],
         'Дата решения':[],'Решение':[],'Ссылка на приказ':[]}

values['Название по'] = ['' for element in range(num)]
values['Ссылка на ПО'] = ['' for element in range(num)]
values['Название организации'] = ['' for element in range(num)]
values['ИНН'] = ['' for element in range(num)]
values['Сведения об исключительном праве'] = ['' for element in range(num)]
values['Сайт'] = ['' for element in range(num)]
values['Альтернатив'] = ['' for element in range(num)]
values['Класс по'] = ['' for element in range(num)]
values['Вид организации'] = ['' for element in range(num)]
values['Все продукты организации'] = ['' for element in range(num)]
values['Дата регистрации'] = ['' for element in range(num)]
values['Рег.номер ПО'] = ['' for element in range(num)]
values['Дата решения'] = ['' for element in range(num)]
values['Решение'] = ['' for element in range(num)]
values['Ссылка на приказ'] = ['' for element in range(num)]


# In[5]:




# создание словаря для передачи его в последствии датафрейму в пандас
values = {'Название по': [], 'Ссылка на ПО':[], 'Вид организации':[],'Название организации': [], 'Все продукты организации':[], 
          'ИНН': [],'Сведения об исключительном праве':[],'Альтернатив': [], 'Класс по': [],  'Сайт': [], 'Дата регистрации':[], 'Рег.номер ПО':[],
         'Дата решения':[],'Решение':[],'Ссылка на приказ':[]}

values['Название по'] = ['' for element in range(num)]
values['Ссылка на ПО'] = ['' for element in range(num)]
values['Название организации'] = ['' for element in range(num)]
values['ИНН'] = ['' for element in range(num)]
values['Сведения об исключительном праве'] = ['' for element in range(num)]
values['Сайт'] = ['' for element in range(num)]
values['Альтернатив'] = ['' for element in range(num)]
values['Класс по'] = ['' for element in range(num)]
values['Вид организации'] = ['' for element in range(num)]
values['Все продукты организации'] = ['' for element in range(num)]
values['Дата регистрации'] = ['' for element in range(num)]
values['Рег.номер ПО'] = ['' for element in range(num)]
values['Дата решения'] = ['' for element in range(num)]
values['Решение'] = ['' for element in range(num)]
values['Ссылка на приказ'] = ['' for element in range(num)]


# In[6]:



j = 0
for i in range(num0, num1):
    url = content[i].strip()
    print(url)
    print(str(i+1) + ' of ' + str(num1))
    req = requests.get(url, verify=False).text
    soup = BeautifulSoup(req, 'lxml')
    # 1 название ПО
    soft = soup.find('h1', id='pagetitle').text
    print(soft + '\n')
    values['Название по'][j] = soft
    #15 ссылка на ПО
    values['Ссылка на ПО'][j] = url
    # 2 название организации
    try:
        orgname = soup.find_all('a', title=re.compile("Все продукты"))
    except AttributeError:
        orgname = ""
        pass
    values['Название организации'][j] = '::'.join([i.text.strip() for i in orgname])
    # 3 ИНН ^(\d{10}|\d{12})$
    try:
        inn = soup.find_all('div', text=re.compile("(\d{10}\s|\d{12}\s)"))
    except AttributeError:
        inn = ''
        pass
    #инн может быть несколько, например в случае 4 правообладателей-людей, поэтому инн в списке
    values['ИНН'][j] = '::'.join([i.text.strip() for i in inn])
    # 4 альтернативное название продукта
    try:
        altname = str(soup.find('span', text=re.compile("Альтернативные наименования:")).find_parent('div')).split('<br/>')
        altname = [x.strip() for x in altname]
        altname = re.sub('''<div style="margin-bottom: 16px;">\n<span style="font-size: 15px; color: #777777; display: block; font-weight: bold;">Альтернативные наименования:</span>''','',
                         altname[0]).strip() +'::'+ "::".join(altname[1:-1])
        altname = re.sub('</div>','', altname.strip('::')).strip()
    except AttributeError:
        altname = ""
        pass
    values['Альтернатив'][j] = altname.strip()
    # 5 Класс по
    try:
        softclas = soup.find('span', text=re.compile("Класс ПО:")).find_parent('div').find_all('font')
        softclass = '::'.join([x.text for x in softclas])
    except AttributeError:
        softclass = ""
        pass
    values['Класс по'][j] = softclass
    # 6 сайт производителя
    try:
        site = soup.find('span', text=re.compile("Сайт производителя:")).find_parent('div').find('a').get('href')
    except AttributeError:
        site = ""
        pass
    values['Сайт'][j] = site
    # 7 вид организации
    try:
        type_of_organization = soup.find_all("h5", attrs={ "style" : "font-size: 20px; margin-bottom: 12px;"})
        type_of_organization = '::'.join([x.text.strip() for x in type_of_organization])
    except AttributeError:
        type_of_organization = ""
        pass
    values['Вид организации'][j] = type_of_organization
    # 8 все продукты организации
    try:
        all_products = ['https://reestr.digital.gov.ru'+x.get('href') for x in soup.find_all('a', title=re.compile('Все продукты'))]
    except AttributeError:
        all_products = ""
        pass
    values['Все продукты организации'][j] = '::'.join(all_products)
    # 9 дата регистрации
    try:
        date_of_registration = soup.find('span', text=re.compile("Дата регистрации:")).find_parent('div').text
        temp = re.sub('Дата регистрации:', '', date_of_registration).strip()
        temp2 = ' '.join([x for x in temp.split(' ') if x!='']).split(' ')
        if (len(temp2[0])==1):
            temp2[0] = '0'+temp2[0]
        temp3 = '.'.join([temp2[0],months.get(temp2[1]),temp2[2]])
    except AttributeError:
        temp3 = ""
        pass
    values['Дата регистрации'][j] = temp3
    # 10 регистрационный номер ПО
    try:
        reg_number = soup.find('span', text=re.compile("Рег. номер ПО:")).find_parent('div').text
        r = re.sub('Рег. номер ПО:', '', reg_number).strip()
    except AttributeError:
        r = ""
        pass
    values['Рег.номер ПО'][j] = r
    # 11 дата решения
    try:
        date_of_decision = soup.find('span', text=re.compile("Дата решения")).find_parent('div').text
        tempp = re.sub('Дата решения уполномоченного органа:', '', date_of_decision).strip()
        tempp2 = ' '.join([x for x in tempp.split(' ') if x!='']).split(' ')
        if (len(tempp2[0])==1):
            tempp2[0] = '0'+tempp2[0]
        tempp3 = '.'.join([tempp2[0],months.get(tempp2[1]),tempp2[2]])
    except AttributeError:
        tempp3 = ""
        pass
    values['Дата решения'][j] = tempp3
    # 12 решение
    try:
        decision = soup.find('span', text=re.compile("Решение уполномоченного")).find_parent('div').text
    except AttributeError:
        decision = ""
        pass
    values['Решение'][j] = re.sub('Решение уполномоченного органа:', '', decision).strip()
    # 13 ссылка на приказ минкомсвязи
    try:
        link = soup.find('span', text=re.compile("Ссылка на приказ")).find_parent('div').find('a').get('href')
    except AttributeError:
        link = ""
        pass
    values['Ссылка на приказ'][j] = link
    # 14 сведения об исключительном праве
    try:
        svedeniya = soup.find('p', attrs = {'style':"line-height: 28px;"}).text.strip().replace('\n', '')
    except AttributeError:
        svedeniya = ''
        pass
    values['Сведения об исключительном праве'][j] = svedeniya
    j = j + 1
    if j%frame ==0:
        print(f'SLEEP {seconds} SECONDS')
        time.sleep(seconds)
print("Парсинг прошел успешно. Записываю в файл")        


# In[7]:


df = pd.DataFrame(values)
columns = ['Наименование ПО', 'Ссылка на запись','Вид правообладателя',
'Название правообладателя','Ссылка на все записи правообладателя','ИНН','Сведения об исключительном праве','Альтернативные наименования','Класс ПО','Сайт производителя',
'Дата регистрации','Рег.номер ПО','Дата решения уполномоченного органа','Решение уполномоченного органа','Ссылка на приказ Минкомсвязи']
df.columns = columns
if format_ == 1:
    df.to_excel(f'{filename}.xlsx', index = False)
elif format_ == 2:
    df.to_csv(f'{filename}.csv', index = False)
else:
    df.to_excel(f'{filename}.xlsx', index = False)
    df.to_csv(f'{filename}.csv', index = False)
print('Запись файла произошла успешно!')


# In[ ]:




