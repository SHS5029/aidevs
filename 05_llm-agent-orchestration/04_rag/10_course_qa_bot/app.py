"""교육과정 Q&A를 브라우저에서 사용할 수 있는 FastAPI 서버입니다."""

import asyncio
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent


def _load_answer_module() -> ModuleType:
    module_path = ROOT / "07_ollama_rag_answer.py"
    spec = importlib.util.spec_from_file_location("course_qa_answer", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"답변 모듈을 불러올 수 없습니다: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


answer_module = _load_answer_module()
answer_course_question: Callable[[str], dict[str, Any]] = (
    answer_module.answer_course_question
)

app = FastAPI(title="AI 캠퍼스 교육과정 Q&A", version="1.0.0")


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI 캠퍼스 교육과정 Q&A</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, Pretendard, system-ui, sans-serif; }
    * { box-sizing: border-box; }
    body {
      margin: 0; min-height: 100vh; display: grid; place-items: center;
      background: radial-gradient(circle at top, #263765 0, #101528 46%, #080b14 100%);
      color: #f6f7fb;
    }
    main {
      width: min(760px, calc(100% - 32px)); padding: 32px;
      border: 1px solid rgba(255,255,255,.12); border-radius: 24px;
      background: rgba(13,18,34,.88); box-shadow: 0 24px 80px rgba(0,0,0,.38);
      backdrop-filter: blur(18px);
    }
    .eyebrow { color: #91a9ff; font-size: 13px; font-weight: 800; letter-spacing: .12em; }
    h1 { margin: 10px 0 8px; font-size: clamp(27px, 5vw, 42px); line-height: 1.12; }
    .lead { margin: 0 0 26px; color: #b7c0d8; line-height: 1.65; }
    form { display: flex; gap: 10px; }
    input {
      flex: 1; min-width: 0; padding: 15px 17px; border: 1px solid #3b4668;
      border-radius: 13px; background: #0b1020; color: white; font-size: 16px;
      outline: none;
    }
    input:focus { border-color: #8ba3ff; box-shadow: 0 0 0 3px rgba(139,163,255,.15); }
    button {
      padding: 0 22px; border: 0; border-radius: 13px; background: #8ba3ff;
      color: #101426; font-size: 15px; font-weight: 800; cursor: pointer;
    }
    button:disabled { cursor: wait; opacity: .6; }
    .examples { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0 0; }
    .example {
      padding: 8px 11px; border: 1px solid #303b5d; border-radius: 999px;
      background: transparent; color: #c8d1e8; font-size: 13px; font-weight: 600;
    }
    #result { display: none; margin-top: 26px; padding-top: 22px; border-top: 1px solid #29324d; }
    #answer { white-space: pre-wrap; line-height: 1.75; font-size: 17px; }
    .meta { margin-top: 18px; padding: 14px; border-radius: 12px; background: #0a0f1e; }
    .label { margin-bottom: 5px; color: #8ba3ff; font-size: 12px; font-weight: 800; }
    #sources, #notice { color: #aeb9d2; font-size: 13px; line-height: 1.55; }
    #notice:empty, #notice:empty + * { display: none; }
    @media (max-width: 600px) { main { padding: 23px; } form { flex-direction: column; } button { padding: 14px; } }
  </style>
</head>
<body>
  <main>
    <div class="eyebrow">2026 AI CAMPUS · RAG</div>
    <h1>교육과정 Q&A</h1>
    <p class="lead">OT 자료를 pgvector로 검색하고 Ollama가 근거 페이지와 함께 답합니다.</p>
    <form id="ask-form">
      <input id="question" maxlength="500" autocomplete="off" placeholder="예: 수료하려면 출석률이 얼마나 되어야 하나요?" required>
      <button id="submit" type="submit">질문하기</button>
    </form>
    <div class="examples">
      <button class="example" type="button">교육 기간과 시간은?</button>
      <button class="example" type="button">개인 프로젝트가 가능한가요?</button>
      <button class="example" type="button">훈련장려금 기준은?</button>
    </div>
    <section id="result" aria-live="polite">
      <div class="label">답변</div>
      <div id="answer"></div>
      <div class="meta">
        <div class="label">출처</div>
        <div id="sources"></div>
      </div>
      <div class="meta" id="notice-box">
        <div class="label">안내</div>
        <div id="notice"></div>
      </div>
    </section>
  </main>
  <script>
    const form = document.querySelector('#ask-form');
    const input = document.querySelector('#question');
    const submit = document.querySelector('#submit');
    const result = document.querySelector('#result');
    const answer = document.querySelector('#answer');
    const sources = document.querySelector('#sources');
    const notice = document.querySelector('#notice');
    const noticeBox = document.querySelector('#notice-box');

    document.querySelectorAll('.example').forEach((button) => {
      button.addEventListener('click', () => {
        input.value = button.textContent;
        input.focus();
      });
    });

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      submit.disabled = true;
      submit.textContent = '답변 중…';
      result.style.display = 'block';
      answer.textContent = 'OT 근거를 검색하고 있습니다…';
      sources.textContent = '';
      notice.textContent = '';
      noticeBox.style.display = 'none';
      try {
        const response = await fetch('/api/ask', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({question: input.value.trim()}),
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || '답변을 생성하지 못했습니다.');
        answer.textContent = data.answer;
        sources.textContent = data.sources.length ? data.sources.join('\\n') : '관련 근거 없음';
        if (data.notice) {
          notice.textContent = data.notice;
          noticeBox.style.display = 'block';
        }
      } catch (error) {
        answer.textContent = error.message;
        sources.textContent = '서버 로그를 확인하세요.';
      } finally {
        submit.disabled = false;
        submit.textContent = '질문하기';
      }
    });
  </script>
</body>
</html>"""


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "collection": answer_module.COLLECTION,
        "model": answer_module.CHAT_MODEL,
    }


@app.post("/api/ask")
async def ask(request: QuestionRequest) -> dict[str, Any]:
    try:
        return await asyncio.to_thread(answer_course_question, request.question)
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail="RAG 서비스에 연결할 수 없습니다. Ollama와 pgvector 상태를 확인하세요.",
        ) from error
