"""간단한 FastAPI 온라인 게시판.

실행:
    python -m uvicorn board:app --reload
"""

from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Simple Online Board")
KST = timezone(timedelta(hours=9))


class PostCreate(BaseModel):
    """게시글 작성 요청 형식입니다."""

    title: str = Field(min_length=1, examples=["FastAPI 게시판 시작"])
    content: str = Field(min_length=1, examples=["첫 번째 게시글입니다."])


class PostUpdate(BaseModel):
    """게시글 수정 요청 형식입니다."""

    id: int = Field(ge=1)
    title: str = Field(min_length=1, examples=["수정된 제목"])
    content: str = Field(min_length=1, examples=["수정된 내용입니다."])


posts = {
    1: {
        "id": 1,
        "title": "FastAPI 게시판 시작",
        "content": "첫 번째 게시글입니다.",
        "created_at": "2026-07-15T00:00:00+00:00",
        "updated_at": "2026-07-15T00:00:00+00:00",
    }
}
next_post_id = 2


def current_time() -> str:
    """현재 KST 시각을 ISO 8601 문자열로 반환합니다."""

    return datetime.now(KST).isoformat()


@app.get("/posts/list")
def list_posts():
    """게시글을 최신 수정일 순서로 조회합니다."""

    post_list = sorted(
        posts.values(),
        key=lambda post: post["updated_at"],
        reverse=True,
    )
    return {"data": post_list}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    """게시글 하나를 조회합니다."""

    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"data": posts[post_id]}


@app.post("/posts/create", status_code=201)
def create_post(post: PostCreate):
    """새 게시글을 작성합니다."""

    global next_post_id

    created_at = current_time()
    new_post = {
        "id": next_post_id,
        "title": post.title,
        "content": post.content,
        "created_at": created_at,
        "updated_at": created_at,
    }
    posts[next_post_id] = new_post
    next_post_id += 1

    return {"message": "post created", "data": new_post}


@app.put("/posts/update")
def update_post(post: PostUpdate):
    """기존 게시글을 수정합니다."""

    if post.id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    posts[post.id] = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": posts[post.id]["created_at"],
        "updated_at": current_time(),
    }
    return {"message": "post updated", "data": posts[post.id]}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    """게시글을 삭제합니다."""

    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Post not found")

    deleted = posts.pop(post_id)
    return {"message": "post deleted", "data": deleted}
