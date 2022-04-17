
import aiohttp
import asyncio
import ssl
import certifi
from config import get_secret
import os
import aiofiles
# fetch 함수를 만들어 각각의 페이지에 대해 동시에 스크래핑 진행할 것


async def img_downloader(session, img):
    # print(img)
    img_folder, img_name = os.path.split(img)
    print(img_name)

    os.makedirs("./images/", exist_ok=True)
    # 이미지 url을 열었을 때, status가 양호(200)하다면, 파일을 쓴다.
    async with session.get(img) as response:
        if response.status == 200:
            # byte
            async with aiofiles.open(f"./images/{img_name}", mode="wb") as file:
                # 인간이 볼 수 있는 형태로 다운로드(바이트 형태로 씀)
                await file.write(await response.read())


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

        # 이미지 다운로더가 동시에 실행
        await asyncio.gather(*[img_downloader(session, img_src) for img_src in images])


async def main():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    BASE_URL = 'https://openapi.naver.com/v1/search/image'
    keyword = 'cat'
    # naver => start == index 의미
    urls = [
        f"{BASE_URL}?query={keyword}&display=20&start={(1+i*20)}" for i in range(10)
    ]

    async with aiohttp.ClientSession(connector=conn) as session:
        # 페이지 하나에 대한 fetch 함수 실행(동시 진행)
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])

# 코루틴 함수
if __name__ == "__main__":
    asyncio.run(main())
