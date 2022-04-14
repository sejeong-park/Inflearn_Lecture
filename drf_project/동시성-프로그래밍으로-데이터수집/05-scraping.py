
import aiohttp
import asyncio
import ssl
import certifi
from config import get_secret
# fetch 함수를 만들어 각각의 페이지에 대해 동시에 스크래핑 진행할 것


async def fetch(session, url, i):
    print(i+1)
    headers = {
        "X-Naver-Client-Id": get_secret('X-Naver-Client-Id'),
        "X-Naver-Client-Secret":  get_secret('X-Naver-Client-Secret')
    }
    # session.get(url, header) -> header은 키값
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item['link'] for item in items]
        print(images)
        # print(result)


async def main():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    BASE_URL = 'https://openapi.naver.com/v1/search/image'
    keyword = 'cat'
    # naver => start == page/
    urls = [
        f"{BASE_URL}?query={keyword}&display=20&start={i}" for i in range(1, 10)
    ]

    async with aiohttp.ClientSession(connector=conn) as session:
        # 페이지 하나에 대한 fetch 함수 실행(동시 진행)
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])

# 코루틴 함수
if __name__ == "__main__":
    asyncio.run(main())
