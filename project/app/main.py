from typing import Optional

from fastapi import FastAPI

# 싱글톤 패턴
app = FastAPI()

# 데코레이터 문법


@app.get("/")
def read_root():
    print("hello world!")
    return {"Hello": "World"}


@app.get("/hello")
def read_fastapi_hello():
    print("hello world!")
    return {"Hello": "FastAPI"}


@app.get("/items/{item_id}/{xyz}")
def read_item(item_id: int, xyz: str, q: Optional[str] = None):
    return {"item_id": item_id, "q": q, "xyz": xyz}
