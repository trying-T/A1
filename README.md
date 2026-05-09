# A1 Repair Knowledge System

基于多模态大模型的设备检修知识检索与作业辅助系统。

当前版本已完成一条可演示的 RAG 最小闭环：

1. 上传设备检修资料。
2. 解析并切分文档内容。
3. 建立向量索引。
4. 基于真实 embedding 检索知识片段。
5. 调用 OpenAI-compatible 大模型生成结构化检修建议。
6. 输出可追溯 sources 和安全提醒。

## 项目定位

本项目面向设备检修场景，重点解决以下问题：

- 检修知识分散在手册、案例和经验中，难以快速检索。
- 新人检修缺少标准化作业指导和安全提醒。
- 故障问答结果难以沉淀为可追踪的检修记录。

## 当前目录说明

- `docs/`：项目文档、范围说明、系统架构、后续答辩材料。
- `data/`：演示资料、检索问题、测试报告和本地运行数据。
- `backend/`：FastAPI 后端，包含文档入库、向量检索和 RAG 问答服务。
- `frontend/`：React + Vite 前端，当前重点支持知识库操作。
- `scripts/`：检索质量测试和 RAG 问答测试脚本。
- `changelog/`：版本变更记录。

## 推荐开发顺序

1. 配置 `.env` 中的 embedding 与 LLM 参数。
2. 上传或准备 `data/uploads/` 下的测试资料。
3. 按 `upload -> parse -> chunk -> index -> search` 验证检索链路。
4. 运行 `scripts/test_retrieval.py` 检查 Top-K 命中质量。
5. 运行 `scripts/test_rag_chat.py` 检查 RAG 问答和来源追溯。

## 当前状态

当前仓库已完成：

- 文档上传、解析、固定长度 chunk 切分和 SQLite 存储。
- 真实 embedding 接入，支持 `siliconflow` / OpenAI-compatible 调用。
- 本地持久化向量检索，返回 `chunk_id`、`document_id`、`filename` 和相似度分数。
- `POST /api/chat/repair` RAG 检修问答接口，支持 DeepSeek / OpenAI-compatible chat completion。
- 检索测试脚本和 RAG 问答测试脚本，报告输出到 `data/demo/`。
- 前端知识库页面支持上传、解析、切分、入库和状态展示。

当前暂不优化 chunk，不做 Agent，不做复杂权限系统。后续建议在真实检修资料接入后，再评估标题感知或章节感知切分策略。

## 常用命令

```powershell
$env:PYTHONPATH='d:\A1\backend'
python scripts\test_retrieval.py
python scripts\test_rag_chat.py
```

```powershell
$env:PYTHONPATH='d:\A1\backend'
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 版本记录

- `changelog/v0.1.0.md`：完成知识入库、真实 embedding、检索测试和 RAG 检修问答闭环。
