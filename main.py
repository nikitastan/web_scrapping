import json
import re
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


def vacancy_search():
    headers = Headers(browser='firefox', os='win')
    params = {'text': 'python',
              'area': [1, 2],
              'order_by': 'publication_time'
              }
    res = requests.get('https://hh.ru/search/vacancy', headers=headers.generate(), params=params).text
    soup = BeautifulSoup(res, 'html.parser')
    vacancy_list = soup.find_all('div', class_='vacancy-serp-item-body__main-info')
    vacancy_json = {}
    for vacancy in vacancy_list:
        title_tag = vacancy.find('a', class_='serp-item__title')
        company_tag = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer',
                                               'class': "bloko-link bloko-link_kind-tertiary"}).text
        city_tag = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': "bloko-text"}).text
        url = title_tag.attrs['href']
        vacancy_page = requests.get(url, headers=headers.generate()).text
        soup_vacancy_page = BeautifulSoup(vacancy_page, 'html.parser')
        vacancy_description = soup_vacancy_page.find('div', attrs={'data-qa': 'vacancy-description'})
        if not vacancy_description:
            continue
        if re.search('Django|Flask', vacancy_description.text, re.IGNORECASE):
            salary_tag = vacancy.find('span', class_='bloko-header-section-3')
            if salary_tag:
                salary = salary_tag.text
            else:
                salary = 'З/п не указана'
            vacancy_json[title_tag.text] = {'salary': salary, 'company': company_tag, 'city': city_tag, 'link': url}
    return vacancy_json


if __name__ == '__main__':
    with open("vacancy.json", "w", encoding='utf-8') as write_file:
        json.dump(vacancy_search(), write_file)
