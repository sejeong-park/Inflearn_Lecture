from bs4 import BeautifulSoup
import aiohttp
import asyncio
import ssl
import certifi
# fetch 함수를 만들어 각각의 페이지에 대해 동시에 스크래핑 진행할 것


async def fetch(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        cont_thumb = soup.find_all('div', 'cont_thumb')  # 해당 모든 요소들이 리스트 내에 담김
        for cont in cont_thumb:
            title = cont.find("p", "txt_thumb")
            # 타이틀이 반드시 있다고 가정(예외처리)
            if title is not None:
                print(title.text)


async def main():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=ssl_context)
    BASE_URL = 'https://bjpublic.tistory.com/category/%EC%A0%84%EC%B2%B4%20%EC%B6%9C%EA%B0%84%20%EB%8F%84%EC%84%9C'
    urls = [f"{BASE_URL}?page={i}" for i in range(1, 10)]

    async with aiohttp.ClientSession(connector=conn) as session:
        # 페이지 하나에 대한 fetch 함수 실행(동시 진행)
        await asyncio.gather(*[fetch(session, url) for url in urls])

# 코루틴 함수
if __name__ == "__main__":
    asyncio.run(main())
