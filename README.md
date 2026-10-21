# 基于 FastAPI 与 Ollama 的本地大模型服务及自动化测试

本项目是一个轻量级的 AI 应用后端实战 Demo。基于 FastAPI 封装本地 Ollama (Qwen 7B) 大模型，实现了多轮对话、SSE 流式输出，并配套了基于 Pytest 的自动化测试脚本。

## 🚀 核心亮点

- **本地私有化部署**：利用 RTX 4060 显卡环境，通过 Ollama 跑通 Qwen 2.5 7B 模型，实现数据不出本地的 AI 对话。
- **SSE 流式输出**：基于 StreamingResponse 与 yield 生成器，实现逐 Token 推送（打字机效果），提升用户体验。
- **多轮对话管理**：服务端基于 session_id 维护字典上下文，并限制最大历史记录条数，防止 Token 溢出。
- **自动化测试防御**：使用 pytest 编写自动化测试脚本，覆盖正常对话、空值异常、超长文本等边界场景，确保接口稳定性。

## 🛠️ 接口说明

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | /health | 健康检查，Ollama 不可达时返回 503 |
| POST | /chat | 对话接口，stream=true 时走 SSE 流式返回 |
| DELETE | /chat/{session_id} | 清空某个会话的历史 |

**请求体示例：**
`{"prompt": "你好", "session_id": "s1", "stream": false}`

## 💻 怎么运行

1. 确保 Ollama 已安装并拉取模型：`ollama pull qwen2.5:7b`
2. 安装依赖并启动服务：`pip install -r requirements.txt`
3. 启动接口服务：`uvicorn main:app --reload`
4. 打开接口文档进行测试：http://127.0.0.1:8000/docs

## 🧪 运行自动化测试 (Pytest)

本项目包含 `test_llm.py` 测试脚本。在服务启动的前提下，打开新终端执行：
`pip install pytest`
`pytest test_llm.py -v`

**测试覆盖场景：**
- `test_normal_chat`：正常对话接口返回 200 且包含 reply 字段。
- `test_empty_input`：空 Prompt 输入时的接口异常防御。
- `test_long_input`：超长文本（千字级别）输入时的接口稳定性验证。

> 实测在 RTX 4060 环境下，3 个用例执行耗时约 9.89s，全部 PASSED。

## ⚙️ 技术栈

Python 3.9+ / FastAPI / Uvicorn / Requests / Pytest / Ollama# 基于 FastAPI 与 Ollama 的本地大模型服务及自动化测试

本项目是一个轻量级的 AI 应用后端实战 Demo。基于 FastAPI 封装本地 Ollama (Qwen 7B) 大模型，实现了多轮对话、SSE 流式输出，并配套了基于 Pytest 的自动化测试脚本。

## 🚀 核心亮点

- **本地私有化部署**：利用 RTX 4060 显卡环境，通过 Ollama 跑通 Qwen 2.5 7B 模型，实现数据不出本地的 AI 对话。
- **SSE 流式输出**：基于 StreamingResponse 与 yield 生成器，实现逐 Token 推送（打字机效果），提升用户体验。
- **多轮对话管理**：服务端基于 session_id 维护字典上下文，并限制最大历史记录条数，防止 Token 溢出。
- **自动化测试防御**：使用 pytest 编写自动化测试脚本，覆盖正常对话、空值异常、超长文本等边界场景，确保接口稳定性。

## 🛠️ 接口说明

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | /health | 健康检查，Ollama 不可达时返回 503 |
| POST | /chat | 对话接口，stream=true 时走 SSE 流式返回 |
| DELETE | /chat/{session_id} | 清空某个会话的历史 |

**请求体示例：**
`{"prompt": "你好", "session_id": "s1", "stream": false}`

## 💻 怎么运行

1. 确保 Ollama 已安装并拉取模型：`ollama pull qwen2.5:7b`
2. 安装依赖并启动服务：`pip install -r requirements.txt`
3. 启动接口服务：`uvicorn main:app --reload`
4. 打开接口文档进行测试：http://127.0.0.1:8000/docs

## 🧪 运行自动化测试 (Pytest)

本项目包含 `test_llm.py` 测试脚本。在服务启动的前提下，打开新终端执行：
`pip install pytest`
`pytest test_llm.py -v`

**测试覆盖场景：**
- `test_normal_chat`：正常对话接口返回 200 且包含 reply 字段。
- `test_empty_input`：空 Prompt 输入时的接口异常防御。
- `test_long_input`：超长文本（千字级别）输入时的接口稳定性验证。

> 实测在 RTX 4060 环境下，3 个用例执行耗时约 9.89s，全部 PASSED。

## ⚙️ 技术栈

Python 3.9+ / FastAPI / Uvicorn / Requests / Pytest / Ollama
