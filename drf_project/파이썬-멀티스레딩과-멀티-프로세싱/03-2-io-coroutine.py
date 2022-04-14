# https://docs.python-requests.org/en/master/index.html


import aiohttp
import time
import asyncio
import ssl
import certifi

import os
import threading


async def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = ["https://naver.com", "https://google.com"] * 50

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=conn) as session:
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        # result = await fetcher(session, urls[0])
        # print(result)


if __name__ == "__main__":
    start = time.time()
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    end = time.time()
    print(end - start)  # 15.7
