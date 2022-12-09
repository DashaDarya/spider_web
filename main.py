from async_fetcher import AsyncFetcher
from awesome_parser import AwesomeParser
from work_with_redis import WorkWithRedis

import asyncio


# Имеем начальную ссылку
START_URL = "https://ngs.ru"
START_DEPTH: int = 0
MAX_DEPTH = 1
counter = 0

PHRASE_TO_SEARCH = "снег"

# Формируем список ссылок из начальной
urls_list = [(START_URL, START_DEPTH)]

# Формируем множество уникальных ссылок
CRAWLED_URLS = set()
CRAWLED_URLS.add(START_URL)


# Создаем индекс
redis_object, search_object = WorkWithRedis.create_index_redis()


# Берём первую из списка ссылку
while len(urls_list) != 0:
    # Берем пачку из первых 10 ссылок
    part_of_urls_list = urls_list[:10]
    print(f"Processing {part_of_urls_list} ...")
    # Удаляем эти ссылки из основного списка
    urls_list = urls_list[10:]
    
    # UrlInfo(
    #     url="ngs.ru",
    #     depth=0,
    #     text="",
    #     status_code=0
    # )

    # Получаем список из 10 кортежей (status, text, url, depth) с текстами страничек
    answer_list = asyncio.run(AsyncFetcher.get_texts_from_pages(part_of_urls_list))

    

    while len(answer_list) != 0:
        counter += 1
        current = answer_list.pop(0)
        status_code, text, current_url, current_depth = current

        # Рабираем текст 
        #  Получаем заголовок и тело
        page_info = AwesomeParser.get_title_and_body_from_html_str(text)
        print(page_info.title)


        # Сохраняем данные в хранилище
        s = WorkWithRedis.save_to_redis(redis_object, counter, page_info, current_url)
        print(s)

        # Проверяем глубину, чтобы ограничить глубину поиска
        if current_depth == MAX_DEPTH:
            continue

        # Определяем все ссылки на странице.
        links = AwesomeParser.get_all_links_from_page(text, current_url)
        print(len(links))

        depth = current_depth + 1

        # Записываем новые ссылки в список.
        for link in links:
            if link in CRAWLED_URLS:
                continue
            else:
                urls_list.append((link, depth))
                CRAWLED_URLS.add(link)

    #  Повторяем все действия для каждой странички

# TODO: Находим ресурсы с нужной нам фразой
print("_________________________________________________________")

