# Ollama-FastAPI-Demo

用 FastAPI 封装本地 Ollama（Qwen 7B），支持**多轮对话**（服务端保存上下文）与**流式输出**（SSE）。

## 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | /health | 健康检查，Ollama 不可达时返回 503 |
| POST | /chat | 对话接口，`stream=true` 时走 SSE 流式返回 |
| DELETE | /chat/{session_id} | 清空某个会话的历史 |

请求体示例：`{"prompt": "你好", "session_id": "s1", "stream": false}`

## 怎么运行

```bash
# 1. 确保 Ollama 已安装并拉取模型（7B 4bit 量化版约 4.5GB）
ollama pull qwen2.5:7b

# 2. 安装依赖并启动
pip install -r requirements.txt
uvicorn main:app --reload

# 3. 打开接口文档测试
# http://127.0.0.1:8000/docs
```

## 多轮对话（同一个 session_id 即同一会话）

```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"prompt\":\"记住数字 42\",\"session_id\":\"s1\"}"
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"prompt\":\"我刚才让你记住几?\",\"session_id\":\"s1\"}"
# 第二句能答出 42，说明上下文生效
```

## 流式输出（SSE，逐 token 返回）

```bash
curl -N -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"prompt\":\"写一首关于郑州的短诗\",\"stream\":true}"
```

## 技术点

- **Pydantic 数据校验**：`ChatRequest` 字段缺失或类型不对，FastAPI 自动返回 422，脏数据进不到模型
- **异常防御**：`/health` 用 try/except 捕获 Ollama 不可达，返回 503 而不是崩溃
- **多轮上下文**：服务端用 dict 按 `session_id` 保存历史，每次请求带最近 20 条发给模型（模型本身无状态）
- **流式输出**：`StreamingResponse` + `yield` 逐 token 推送 SSE，前端可做打字机效果

## 依赖环境

Python 3.9+、FastAPI、uvicorn、requests、Ollama（本地模型 qwen2.5:7b）

## 仓库

https://github.com/ysuerde/Ollama-FastAPI-Demo
