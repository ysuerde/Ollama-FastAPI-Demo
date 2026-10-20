# -*- coding: utf-8 -*-
"""
Ollama-FastAPI-Demo
用 FastAPI 封装本地 Ollama（Qwen 7B）：支持多轮对话（服务端保存上下文）与流式输出（SSE）。

运行：
    uvicorn main:app --reload
接口文档：
    http://127.0.0.1:8000/docs
"""
import json
import os
from typing import Dict, List

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
MAX_HISTORY = 20  # 每个会话最多保留的消息条数，防止上下文无限增长

app = FastAPI(title="Ollama-FastAPI-Demo")

# 会话历史：session_id -> [{"role": "user"/"assistant", "content": "..."}]
sessions: Dict[str, List[dict]] = {}


class ChatRequest(BaseModel):
    """请求体：session_id 区分会话（多轮对话），stream 控制是否流式返回。"""
    prompt: str                    # 用户这次输入
    session_id: str = "default"    # 会话标识，相同即同一轮对话
    stream: bool = False           # 传 true 走 SSE 流式输出


@app.get("/health")
def health():
    """健康检查：Ollama 未启动时返回 503，方便运维监控，而不是让服务直接崩。"""
    try:
        requests.get(OLLAMA_HOST + "/api/tags", timeout=3).raise_for_status()
        return {"status": "ok", "model": MODEL}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Ollama 不可达: %s" % e)


def _messages(req: ChatRequest):
    """把本次输入追加进会话历史，返回完整的 messages（多轮对话的核心）。"""
    history = sessions.setdefault(req.session_id, [])
    history.append({"role": "user", "content": req.prompt})
    sessions[req.session_id] = history[-MAX_HISTORY:]  # 只保留最近 N 条
    return sessions[req.session_id]


@app.post("/chat")
def chat(req: ChatRequest):
    messages = _messages(req)
    payload = {"model": MODEL, "messages": messages, "stream": req.stream}

    # 流式分支：逐 token 通过 SSE 推送
    if req.stream:
        def event_stream():
            reply = ""
            with requests.post(
                OLLAMA_HOST + "/api/chat", json=payload, stream=True, timeout=300
            ) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        token = json.loads(line).get("message", {}).get("content", "")
                        reply += token
                        yield "data: " + json.dumps({"content": token}, ensure_ascii=False) + "\n\n"
            sessions[req.session_id].append({"role": "assistant", "content": reply})
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    # 非流式分支：一次性返回完整回复
    r = requests.post(OLLAMA_HOST + "/api/chat", json=payload, timeout=300)
    r.raise_for_status()
    reply = r.json().get("message", {}).get("content", "")
    sessions[req.session_id].append({"role": "assistant", "content": reply})
    return {"session_id": req.session_id, "reply": reply}


@app.delete("/chat/{session_id}")
def clear(session_id: str):
    """清空某个会话的历史，方便重新开始。"""
    sessions.pop(session_id, None)
    return {"cleared": session_id}
