import requests
from bs4 import BeautifulSoup
import os

def download_images(query, limit=30):
    # Проверка и создание папки для сохранения изображений
    if not os.path.exists(query):
        os.makedirs(query)
    
    # Счетчик скачанных изображений
    count = 0
    
    # Параметры запроса
    start = 0
    while count < limit:
        # Запрос к Google Images
        url = f"https://www.google.com/search?q={query}&tbm=isch&start={start}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        # Парсинг HTML с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Скачивание изображений
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url:
                try:
                    img_response = requests.get(img_url)
                    with open(os.path.join(query, f"image_{count+1}.jpg"), "wb") as f:
                        f.write(img_response.content)
                    print(f"Изображение {count+1} скачано: {img_url}")
                    count += 1
                except Exception as e:
                    print(f"Не удалось скачать изображение {count+1}: {img_url} - {e}")
                
                if count >= limit:
                    break
        
        # Увеличиваем счетчик для следующего запроса
        start += 20

if __name__ == "__main__":
    query = input("Введите запрос для поиска изображений: ")
    limit = int(input("Введите количество изображений для скачивания: "))
    
    download_images(query, limit)
