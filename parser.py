import requests as req
import time
import datetime
from bs4 import BeautifulSoup
import os

url = os.environ.get('URL')
url_write = os.environ.get('URL_WRITE')
url_reg = os.environ.get('URL_REG')
data = {os.environ.get('CHECK'): '1'}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
timeout = 5
doclist = os.environ.get('DOCTORS')
doctors = doclist.split(',')
lastName = os.environ.get('LAST_NAME').encode('windows-1251')
firstName = os.environ.get('FIRST_NAME').encode('windows-1251')
middleName = os.environ.get('MIDDLE_NAME').encode('windows-1251')
birthday = os.environ.get('BIRTHDAY')

print('##### НАЧАЛО РАБОТЫ #####')
while True:
    try:
        r = req.post(url, headers=headers, data=data, timeout=timeout)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find('table', width="100%")
            if table is not None:
                print('##### ТАЛОНЫ НАЙДЕНЫ #####')
                tds = table.findAll('td')
                print(tds)
                checkDoctor = False
                for td in tds:
                    attr = getattr(td, 'attrs')
                    if attr.get('class') == ['lineRazd']:
                        checkDoctor = False
                        for i in range(len(doctors)):
                            if getattr(td, 'text').find(doctors[i]) != -1:
                                checkDoctor = True
                                print('##### ВРАЧ НАЙДЕН #####')
                                break
                    elif checkDoctor:
                        attr = td.find('input', type='checkbox')
                        if attr is not None:
                            attr = getattr(attr, 'attrs')
                            print('##### ВЫБОР ТАЛОНОВ #####')
                            data = {attr['name']: '1'} 
                            r = req.post(url_write, headers=headers, data=data, timeout=timeout)
                            if r.status_code == 200:
                                print('##### РЕГИСТРИРУЕМСЯ #####')
                                soup = BeautifulSoup(r.text, "html.parser")
                                attr = soup.findAll('input', type='hidden')
                                data.clear()
                                for i in range(len(attr)):
                                    item = getattr(attr[i], 'attrs')
                                    data[item['name']] = item['value']
                                data['vlRadio'] = '1'
                                data['vs60Fam'] = lastName
                                data['vs60Im'] = firstName
                                data['vs60Otc'] = middleName
                                data['vs10Date'] = birthday
                                r = req.post(url_reg, headers=headers, data=data, timeout=timeout)
                                if r.status_code == 200:
                                    soup = BeautifulSoup(r.text, "html.parser")
                                    attr = soup.find('table', width='100%')
                                    print(attr.text)
                                    exit()
                                else:
                                    print(r.status_code + ' !!!!! ОШИБКА ЗАПРОСА К ФОРМЕ РЕЗУЛЬТАТА !!!!!')
                            else:
                                print(r.status_code + ' !!!!! ОШИБКА ЗАПРОСА К ФОРМЕ РЕГИСТРАЦИИ !!!!!')
            elif soup.form.text.find('Талоны к указанному врачу отсутствуют') != -1:
                now = datetime.datetime.now()
                print(now.strftime("%H:%M:%S ") + '##### ТАЛОНОВ НЕТ #####')
        else:
            print(r.status_code + ' !!!!! ОШИБКА ЗАПРОСА К САЙТУ !!!!!')
    except Exception as e:
        print(type(e))
    time.sleep(30);
print('##### ЗАВЕРШЕНИЕ РАБОТЫ #####')
exit()
