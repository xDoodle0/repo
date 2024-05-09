import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def extract_links_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and (href.startswith('http') or href.startswith("/")):
            if href.startswith("/"):
                hrefresult="https://znanierussia.ru"+href
                links.append(hrefresult)
            else:
                links.append(href)
    
    return links

def check_and_save_working_link(link_to_check):
    try:
        response = requests.get(link_to_check)
        response.raise_for_status()  
        return "Ссылка работает."
    except requests.exceptions.HTTPError as errh:
        print("HTTP ошибка:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Ошибка подключения:", errc)
    except requests.exceptions.Timeout as errt:
        print("Время подключения истекло:", errt)
    except requests.exceptions.RequestException as err:
        print("Что-то пошло не так", err)
    
    return None

def get_creation_date(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tags = soup.find_all('meta')

        for tag in meta_tags:
            if 'name' in tag.attrs and tag.attrs['name'].lower() == 'date':
                return tag.attrs.get('content')
            elif 'property' in tag.attrs and tag.attrs['property'].lower() == 'article:published_time':
                return tag.attrs.get('content')

        return "Creation date not found in metadata."
    except Exception as e:
        return str(e)
    
def get_date_difference(link):
    date_format = "%Y-%m-%dT%H:%M:%SZ" 
    date_format2 = "%Y-%m-%d %H:%M:%S.%f"  
    date1 = datetime.strptime(get_creation_date(link), date_format)
    date2 = datetime.strptime(str(datetime.now()), date_format2)
    difference_in_years = abs((date1 - date2).days)//365
    print(f"Разница между датами в годах: {difference_in_years} лет")

    
def save_single_link(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup.prettify()

def wayback(link, filename):
    url = "https://web.archive.org/web/20230929100904/" + link
    with open( filename+".txt","w") as file:
        file.write(url + "\n")

    
filename = str(0)
print("Напишите цифру для выбора действия.")
print("1 - Поиск и архивация ссылок" + "\n")
print("2 - Проверка работоспособности ссылки и добавление копии " + "\n")
print("3 - Сохранение информации и контента " + "\n")
choice = input()
if choice == str(1):
    print("Введите ссылку на статью, либо название статьи.")
    link = input()
    if link.startswith("https://znanierussia.ru/articles/"):
        linkres = link
    else:
        link.replace(" ", "_")
        linkres = "https://znanierussia.ru/articles/" + link
    links = extract_links_from_website(linkres)
    print("Введите название файла для сохранения ссылок.")
    url = input()
    if url.endswith(".txt"):
        url = url.rstrip(".txt")
    with open(url +".txt","w") as file:
        for link in links:
            file.write(link + "\n")
    print("Ссылки успешно сохранены в файле " + url + ".txt")

if choice == str(2):
    print("Напишите цифру для выбора действия." + "\n")
    print("1 - Одна ссылка" + "\n")
    print("2 - .txt файл ссылок" + "\n")
    ch = input()
    if ch == str(1):
        print("Введите ссылку.")
        link1 = input()
        res = check_and_save_working_link(link1)
        print(res + "\n")
        print("Введите файл для сохранения ссылки на копию")
        filename = input()
        if filename.endswith(".txt"):
            filename = filename.rstrip(".txt")
        wayback(link1, filename)
        print("Ссылки на источник с копиями успешно сохранены в файле " + filename + ".txt")
    if ch == str(2):
        print("Введите название .txt файла с ссылками" + "\n")
        txt = input()
        if txt.endswith(".txt"):
            txt = txt.rstrip(".txt")
        with open(txt + ".txt", "r") as file:
            lines = file.readlines()
        print("Введите файл для сохранения ссылки на копию")
        filename = input()
        if filename.endswith(".txt"):
            filename = filename.rstrip(".txt")
        with open(filename + ".txt","w") as file:
            for line in lines:
                file.write("https://web.archive.org/web/20230929100904/" + line)
        print("Ссылки на источник с копиями успешно сохранены в файле " + filename + ".txt")

if choice == str(3):
    print("Напишите цифру для выбора действия." + "\n")
    print("1 - Одна ссылка" + "\n")
    print("2 - .txt файл ссылок" + "\n")
    ch = input()
    if ch == str(1):
        print("Введите ссылку для сохранения копии страницы")
        link2 = input()
        print("Введите название папки для сохранения страницы")
        dirname = input()
        print("Введите название файла для копии")
        filename = input()
        folder_path = os.getcwd() + "\\" +dirname
        os.makedirs(folder_path, exist_ok=True)
        with open(folder_path + "\\" + filename + ".html","w",encoding="utf-8") as file:
            file.write(save_single_link(link2))
        print("Копия страницы сохранена.")
        
    if ch == str(2):
        print("Введите .txt файл с ссылками")
        txt1 = input()
        if txt1.endswith(".txt"):
            txt1 = txt1.rstrip(".txt")
        print("Введите название папки для сохранения страницы")
        dirname = input()
        folder_path = os.getcwd() + "\\" +dirname
        os.makedirs(folder_path, exist_ok=True)
        with open(txt1 + ".txt","r") as file:
            lines = file.readlines()
            for line in lines:
                print(line)
                with open(folder_path + "\\" + filename + ".html","w",encoding="utf-8") as file:
                    response = requests.get(line)
                    if response.status_code == 200:
                        html_content = response.text
                        soup = BeautifulSoup(html_content, 'html.parser')
                        file.write(str(soup.prettify()))
                        filename = str(int(filename)+1)
        print("Копии страниц сохранена.")
