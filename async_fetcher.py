import aiohttp
import dataclasses
import asyncio

@dataclasses.dataclass
class OurTimeouts:
    retries_count = 3
    connection_timeout = 0.33
    total_timeout = 10

class AsyncFetcher:
    """
    Класс ответсвенный за асинхронное получение HTML страниц
    """
    
    @staticmethod
    async def get_page_text(url: str, depth: int, options = OurTimeouts()) -> tuple[int, str, str, int]:
        for retry_i in range(options.retries_count):
            try:
                timeouts = aiohttp.ClientTimeout(total=options.total_timeout, connect=options.connection_timeout)
                async with aiohttp.ClientSession(timeout=timeouts) as session:
                    async with session.get(url) as response:
                        text = await response.text()
                        return response.status, text, url, depth
            except (aiohttp.ClientConnectionError, aiohttp.ServerTimeoutError) as e:
                print(f"{url} - {e} - {retry_i}")
                await asyncio.sleep(0.25)
                continue
            except Exception as e:
                print(e)
                break

        return 0, "", url, depth


    @staticmethod
    async def get_texts_from_pages(part_of_list: list[tuple], options = OurTimeouts()) -> list[tuple[int, str, str, int]]:
        
        # Я сюда передала список (url, depth)

        tasks_list = []
        for one in part_of_list:
            url = one[0]
            depth = one[1]
            task = asyncio.create_task(AsyncFetcher.get_page_text(url, depth, options))
            tasks_list.append(task)
        answer = await asyncio.gather(*tasks_list, return_exceptions=True)
        return [t for t in answer if isinstance(t, tuple)]


