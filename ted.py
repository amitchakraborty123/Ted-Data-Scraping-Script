'''
Author: Amit Chakraborty
Project: Ted Data Scraping Script
Profile URL: https://github.com/amitchakraborty123
E-mail: mr.amitc55@gmail.com
'''

import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,bn-BD;q=0.8,bn;q=0.7',
    'cookie': '_nu=1677962807; _abby_post15s=b; _abby=KY3lUWSee7NocEu; _abby_hero_form=a; _ga=GA1.2.1083928499.1677962807; _tcn=9360; _gid=GA1.2.1631820280.1678174284; mp_cefc84a7a812fb3bb40d6efadb6b3163_mixpanel=%7B%22distinct_id%22%3A%20%22186ae60841b84-0f025d6c6c823b-26031951-100200-186ae60841c394%22%2C%22%24device_id%22%3A%20%22186ae60841b84-0f025d6c6c823b-26031951-100200-186ae60841c394%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; mnet_session_depth=2%7C1678184649518; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Mar+07+2023+16%3A24%3A46+GMT%2B0600+(Bangladesh+Standard+Time)&version=6.31.0&isIABGlobal=false&hosts=&consentId=93b65cee-8550-4597-aa66-aad8805844aa&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE4Nzc5MTEiLCJhcCI6IjEzODU4Njg0MTMiLCJpZCI6IjRkZTc2YWIwMDY4MWRlYjEiLCJ0ciI6ImVlM2VmNjY5NjNjYzdlMjM1MWE5Y2FhNGNkNTk4Y2YwIiwidGkiOjE2NzgxODQ3NjQ0MzF9fQ==',
    'referer': 'https://www.ted.com/tedx/events?page=27&year=2023',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-ee3ef66963cc7e2351a9caa4cd598cf0-4de76ab00681deb1-01',
    'tracestate': '1877911@nr=0-1-1877911-1385868413-4de76ab00681deb1----1678184764431',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'x-newrelic-id': 'VQ4AVl9SCRABVVhSAwAHVFUD',
    'x-requested-with': 'XMLHttpRequest'
}

# driver = driver_conn()
# ================================================================================
#                         Get Links
# ================================================================================
all_link = []

def get_url():
    print('==================== Getting url ====================')
    url = "https://www.ted.com/tedx/events?page="
    pag = 0

    while True:
        pag += 1
        print(">>>>>>>>>>>>>>>>>>>>>> Page: " + str(pag))
        r = requests.get(url + str(pag), headers=headers)
        time.sleep(4)
        soup = BeautifulSoup(r.content, 'lxml')

        lis = soup.find('table', {'id': 'tedx-events-by-date'}).find('tbody').find_all('tr', {'class': 'tedx-events-table__event'})
        print("Listing here: ", len(lis))
        if len(lis) < 1:
            break
        for li in lis:
            link = ''
            date = ''
            event_name = ''
            type = ''
            location = ''
            space_available = ''
            wencast = ''
            try:
                date = li.find_all('td')[0].text.replace('\n', '').replace('Date', '')
            except:
                pass
            try:
                link = li.find_all('td')[1].find('a')['href']
            except:
                pass
            try:
                event_name = li.find_all('td')[1].find('a').text.replace('\n', '')
            except:
                pass
            try:
                type = li.find_all('td')[1].find('span', {'class': 'tedx-events-table__event-type'}).text.replace('\n', '')
            except:
                pass
            try:
                temp = li.find_all('td')[2]
                soupp = BeautifulSoup(str(temp), 'lxml')
                temp_1 = str(soupp).replace('<br/>', ', ')
                soup = BeautifulSoup(temp_1, 'lxml')
                location = soup.td.text.replace('Location', '').replace('\n', '').strip()
            except:
                pass
            try:
                space_available = li.find_all('td')[3].find('span', {'class': 'screen-reader-text'}).text.replace('\n', ', ').replace('Space avail.', '').strip()
            except:
                pass
            try:
                wencast = li.find_all('td')[4].text.replace('\n', '').replace('Webcast', '').strip()
            except:
                pass
            data = {
                'links': 'https://www.ted.com' + link,
                'Date': date,
                'Event name': event_name,
                'Type': type,
                'Location': location,
                'Space available': space_available,
                'Wencast': wencast,
            }
            # print("Link length", len(link))
            if data not in all_link:
                all_link.append(data)


def get_data():
    all_data = []
    print('=================== Data Scraping ===================')
    print('Total link: ' + str(len(all_link)))
    d = 0
    for item in all_link:
        d += 1
        print('Getting Data: ' + str(d) + ' out of ' + str(len(all_link)))
        link = item['links']
        date = item['Date']
        event_name = item['Event name']
        type = item['Type']
        location = item['Location']
        space_available = item['Space available']
        wencast = item['Wencast']

        r = requests.get(link, headers=headers)
        time.sleep(3)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            organizer_link = ''
            organizer_name = ''
            instance_apply = ''
            full_address = ''
            try:
                temp = soup.find('div', {'class': 'tedx-event-details'}).find('div', {'class': 'section--except-first'}).find_all('div', {'class': 'col-lg-3'})[-1].find_all('div', {'class': 'm3'})[1]
                add_soupp = BeautifulSoup(str(temp), 'lxml')
                temp_1 = str(add_soupp).replace('<br/>', '\n')
                add_soup = BeautifulSoup(temp_1, 'lxml')
                full_address = add_soup.div.text.strip()
            except:
                pass
            try:
                link_list = []
                lis = soup.find('ul', {'class': 'icon-list'}).find_all('li', {'class': 'icon-list__item'})
                for li in lis:
                    lnk = li.find('a')['href']
                    link_list.append(lnk)
                instance_apply = ('\n'.join(link_list))
            except:
                pass
            try:
                org_name_list = []
                lis = soup.find('div', {'class': 'section--minor'}).find_all('div', {'class': 'media__message'})
                for li in lis:
                    temp = li.find('h4')
                    name_soupp = BeautifulSoup(str(temp), 'lxml')
                    temp_1 = str(name_soupp).replace('<br/>', ' ')
                    name_soup = BeautifulSoup(temp_1, 'lxml')
                    nam = name_soup.h4.text.replace('\n', '').strip()
                    org_name_list.append(nam)
                organizer_name = ('\n'.join(org_name_list))
            except:
                pass
            try:
                org_link_list = []
                lis = soup.find('div', {'class': 'section--minor'}).find_all('div', {'class': 'media__message'})
                for li in lis:
                    lnkk = li.find('a')['href']
                    org_link_list.append(lnkk)
                organizer_link = ("https://www.ted.com" + '\n'.join(org_link_list))
            except:
                pass
            if len(str(organizer_name) + str(organizer_link) + str(full_address) + str(instance_apply)) > 1 :
                data = {
                    'Links': link,
                    'Date': date,
                    'Event name': event_name,
                    'Type': type,
                    'Location': location,
                    'Space available': space_available,
                    'Wencast': wencast,
                    'Full address': full_address,
                    'Organizer name': organizer_name,
                    'Organizer link': organizer_link,
                    'Instant_apply & others link': instance_apply,
                }
                all_data.append(data)
                df = pd.DataFrame(all_data)
                df = df.rename_axis("Index")
                df.to_excel('Ted_Data.xlsx')



if __name__ == '__main__':
    get_url()
    get_data()