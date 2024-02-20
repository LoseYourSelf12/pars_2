import os
import requests

def download_images(query, api_key, cx, limit=30):
    # Проверка и создание папки для сохранения изображений
    if not os.path.exists(query):
        os.makedirs(query)
    
    # Счетчик скачанных изображений
    count = 0

    # Параметры запроса к Google Custom Search API
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "searchType": "image",
        "num": min(limit, 10)  # Максимальное количество изображений на один запрос - 10
    }

    # Поиск изображений и скачивание
    while count < limit:
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            results = response.json().get("items", [])

            if not results:
                print("Нет результатов для данного запроса.")
                break

            for result in results:
                img_url = result["link"]
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

            if len(results) < params["num"]:
                print("Достигнуто максимальное количество доступных изображений.")
                break

            params["start"] = int(params.get("start", 1)) + params["num"]
        except Exception as e:
            print(f"Произошла ошибка при выполнении запроса к Google Custom Search API: {e}")
            break

if __name__ == "__main__":
    query = input("Введите запрос для поиска изображений: ")
    api_key = input("Введите ваш API ключ Google: ")
    cx = input("Введите ваш идентификатор поискового движка (CX): ")
    limit = int(input("Введите количество изображений для скачивания: "))
    
    download_images(query, api_key, cx, limit)

# my api: AIzaSyBhjd1PzyuhKKbWQYt40Xp48hHxN8XwgiU
# my cx: 01cf86c9602ba442c