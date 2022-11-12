import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime

from decoratory import benchmark


def get_html(url):
    responce = requests.get(url)
    return responce.text

def get_car_models(html):
    urls = []
    soup = BeautifulSoup(html, 'lxml')
    listing_main = soup.find('div', class_ = 'table-view-list image-view clr label-view')
    cars = listing_main.find_all('div', class_ = 'list-item list-label')
    for car in cars:
        a = car.find('a').get('href')
        model = 'https://www.mashina.kg/' + a
        urls.append(model)
        # print(urls)
    return urls

def get_all_models():
    models = []
    for i in range(1, 1137):
        url = f'https://www.mashina.kg/search/all/?page={i}'
        html = get_html(url)
        cars_models = get_car_models(html)
        models.extend(cars_models)
        print(models)
    return models

def get_page_data(models):
    html = get_html(models)
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h2', class_ = 'name')
    except:
        name = 'Нет имени!'
    container = soup.find('div', class_ = 'seller-comments')
    bio = [tag.text for tag in container.find_all('h2')]
    str_bio = ' '.join(bio)
    listing_main = soup.find('div', class_ = 'table-view-list image-view clr label-view')
    cars = listing_main.find_all('div', class_ = 'list-item list-label')
    for car in cars:
        a = car.find('a').get('href')
        model = 'https://www.mashina.kg/' + a
        price = car.find('div', class_ = 'block price').text
        try:
            image = car.find('img', class_ = 'lazy-image visible').get('src')
        except:
            image = 'Нет картинки!'
    if len(str_bio.strip()) < 10:
        str_bio = container.find('pre').text
    data = {
            'name':name,
            'price':price,
            'image':image, 
            'bio': str_bio
        }
    return data

def write_csv(data):
    with open('mashiny.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'], data['price'], data['image', data['bio']]))
        print(f'{data["name"]} - parced!') 
     
def prepare_csv():
    with open('mashiny.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('Модель', 'Цена', 'Ссылка', 'Описание'))


def make_all(link):
    data = get_page_data(link)
    write_csv(data)   
     
@benchmark
def main():
    prepare_csv()
    models = get_all_models()
    for link in models: # Последовательно
        data = get_page_data(link)
        write_csv(data) 
        
main()
            
  

url = 'https://www.mashina.kg/'
html = get_html(url)
models = get_all_models()
for x in models:
    print(get_page_data(x))