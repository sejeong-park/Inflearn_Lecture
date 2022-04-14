
import asyncio
import time


async def delivery(name, mealtime):
    print(f"{name}에게 배달 완료!")
    await asyncio.sleep(mealtime)
    print(f"{name} 식사 완료, {mealtime} 시간 소요 ...")
    print(f"{name} 그릇 수거 완료")

    return mealtime


async def main():
    # 동시성
    result = await asyncio.gather(
        delivery('A', 1),
        delivery('B', 1),
        delivery('C', 3)
    )

    print(result)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())  # 코루틴 실행하고 결과를 반환할 때
    end = time.time()
    print(end - start)
