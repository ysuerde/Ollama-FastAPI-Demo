# Ollama-FastAPI-Demo

用 FastAPI 封装本地 Ollama（Qwen 7B）的极简对话接口：`GET /health` 健康检查，`POST /chat` 对话。

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

## 依赖环境

Python 3.9+、FastAPI、uvicorn、requests、Ollama（本地模型 qwen2.5:7b）

## 推到 GitHub（两种方式任选）

方式一：命令行（Git Bash / CMD）

```bash
cd Ollama-FastAPI-Demo
git init
git add .
git commit -m "init: FastAPI + Ollama demo"
git branch -M main
git remote add origin https://github.com/你的用户名/Ollama-FastAPI-Demo.git
git push -u origin main
```

方式二：不会 Git 就用网页版——GitHub 新建仓库后，点 "Add file → Upload files"，把这三个文件直接拖进去，点 Commit 即可。
