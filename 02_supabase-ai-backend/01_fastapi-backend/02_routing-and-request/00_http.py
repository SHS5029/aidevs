"""
uvicorn 00_http:app --reload
"""

from fastapi import FastAPI, Request
from dataclasses import dataclass

app = FastAPI(
    title="First FastAPI",
    description="FastAPI 서버의 첫 예제입니다.",
    version="0.0.1",
)


##model data
# 1. Memo
@dataclass
class Memo:
    id : int
    title : str
    content : str


##MOCK DATA
memos = []
memos.append(Memo(
            id=2,
            title="메모 제목2", 
            content="내용2"
            ))
memos.append(Memo(
            id=3,
            title="메모 제목3", 
            content="내용3"
            ))
memos.append(Memo(
            id=4,
            title="메모 제목4", 
            content="내용4"
            ))





@app.get("/memo/get/{memo_id}")
def read_memo(memo_id: int) -> Memo:
    """read_memo"""
    for memo in memos:
        if memo.id == memo_id:
            return memo
    return None

@app.get("/memo/getall")
def read_all_memos()-> list[Memo]:
    """read_all_memos"""
    return memos

@app.post("/memo/post")
def create_memo(memo: Memo):
    """create_memo"""
    memos.append(memo)
    return {"message": "메모를 생성합니다."}

@app.put("/memo/put")
def update_memo():
    """update_memo"""
    return {"message": "메모를 수정합니다."}

@app.delete("/memo/remove")
def remove_memo():
    """remove_memo"""
    return {"message": "메모를 삭제합니다."}