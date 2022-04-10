# https://docs.python-requests.org/en/master/index.html

import requests
import time

import os
import threading
from concurrent.futures import ThreadPoolExecutor


def fetcher(params):
    session = params[0]
    url = params[1]
    print(params)
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    # 해당하는 세션의 응답 반환
    with session.get(url) as response:
        return response.text

# 네이버 url에서 세션을 유지시키고, 세션 안에서 request.get을 통해 데이터를 들고 옴


def main():
    urls = ["https://naver.com", "https://google.com"] * 50

    # max_workers 는 최대 스레드 실행할 개수
    executor = ThreadPoolExecutor(max_workers=10)

    with requests.Session() as session:
        params = [(session, url) for url in urls]
        results = list(executor.map(fetcher, params))
        #result = [fetcher(session, url) for url in urls]
        # session.get(url)    # 세션에 대한 정보 유지
        print(results)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 17.9 # 3.2040
