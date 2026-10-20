# -*- coding: utf-8 -*-
"""

"""
import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

app = FastAPI(title="Ollama-FastAPI-Demo")


class ChatRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    """探测本地 Ollama 是否可达。"""
    try:
        requests.get(OLLAMA_HOST + "/api/tags", timeout=3).raise_for_status()
        return {"status": "ok", "model": MODEL}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Ollama 不可达: %s" % e)


@app.post("/chat")
def chat(req: ChatRequest):
    """把用户输入转给本地模型，返回模型输出。"""
    resp = requests.post(
        OLLAMA_HOST + "/api/generate",
        json={"model": MODEL, "prompt": req.prompt, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    return {"reply": resp.json().get("response", "")}
