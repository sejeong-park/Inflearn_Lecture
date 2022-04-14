# https://docs.python-requests.org/en/master/index.html

import requests
import time

import os
import threading


def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    # 해당하는 세션의 응답 반환
    with session.get(url) as response:
        return response.text

# 네이버 url에서 세션을 유지시키고, 세션 안에서 request.get을 통해 데이터를 들고 옴


def main():
    urls = ["https://naver.com", "https://google.com"] * 50

    with requests.Session() as session:
        result = [fetcher(session, url) for url in urls]
        # session.get(url)    # 세션에 대한 정보 유지
        # print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
