# 系统理解文档

本文用于降低对自动生成代码的“盲盒感”，帮助项目负责人快速理解当前系统到底做了什么、各模块之间怎么配合、出了问题应该从哪里查。本文只描述当前已经实现的主链路，不包含 Agent、多模态、复杂权限等未来能力。

## 1. 当前主链路

系统当前主链路是：

```text
upload -> parse -> chunk -> index -> search -> rag -> workorder
```

对应含义如下：

| 阶段 | 做什么 | 主要落点 |
| --- | --- | --- |
| upload | 上传 PDF、TXT、Markdown 原始资料 | `data/uploads`、`documents` 表 |
| parse | 将原始资料解析为纯文本 | `data/parsed/documents`、`documents.parsed_text_path` |
| chunk | 将纯文本切成知识片段 | `chunks` 表 |
| index | 对 chunk 做 embedding，并写入本地向量存储 | `data/vector_db/chroma/chunks.json` |
| search | 用户问题向量化后检索相关 chunk | `/api/retrieval/search` |
| rag | 将检索片段拼入 prompt，调用 LLM 生成结构化检修建议 | `/api/chat/repair` |
| workorder | 将一次 RAG 结果沉淀为检修记录 | `workorders` 表 |

这个链路的核心设计原则是：先让知识能入库、能检索、能追溯，再让模型基于检索结果回答，最后把回答沉淀成作业记录。

## 2. 后端 Service 职责

### `DocumentService`

文件位置：`backend/app/services/document_service.py`

负责文档生命周期流转：

- `save_upload`：保存上传文件，写入 `documents` 表，初始状态为 `uploaded`。
- `parse_document`：读取原始文件，调用 `ParserService` 解析为文本，状态更新为 `parsed`。
- `chunk_document`：读取解析文本，调用 `ChunkService` 切分，写入 `chunks` 表，状态更新为 `chunked`。
- `index_document`：读取 `chunks`，调用 `EmbeddingService` 生成向量，写入 `ChromaStore`，状态更新为 `indexed`。

稳定性处理：

- 重新 parse/chunk/index 前会清理该文档旧 chunks 和旧向量记录。
- 处理失败时将 `documents.status` 置为 `failed`，并写入 `error_message`。

### `ParserService`

文件位置：`backend/app/services/parser_service.py`

负责把不同文件类型转成纯文本：

- PDF：使用 `pypdf.PdfReader` 提取文本。
- TXT/Markdown：按 `utf-8`、`utf-8-sig`、`gb18030`、`gbk`、`utf-16` 尝试读取。

限制：

- 扫描版 PDF 或图片型 PDF 目前无法 OCR。
- 表格、图片、复杂版式不会被结构化还原。

### `ChunkService`

文件位置：`backend/app/services/chunk_service.py`

负责文本切分：

- 默认 `chunk_size = 700`。
- 默认 `overlap = 100`。
- 采用固定长度滑窗切分。

当前策略适合 MVP 验证，但不是最终最优方案。真实工程文档中如果章节结构很强，后续应升级为章节感知或标题感知切分。

### `EmbeddingService`

文件位置：`backend/app/services/embedding_service.py`

负责统一封装 embedding：

- `EMBEDDING_PROVIDER=mock` 时使用本地 mock embedding。
- `EMBEDDING_PROVIDER=siliconflow` 或 `openai_compatible` 时调用 OpenAI-compatible embeddings API。
- 对外提供 `embed_text` 和 `embed_texts`。

稳定性处理：

- 真实 provider 调用失败会抛出 `EmbeddingError`。
- 不会静默 fallback 到 mock。
- 错误信息包含 provider/model，便于定位，但不暴露 API key。

### `ChromaStore`

文件位置：`backend/app/vectorstore/chroma_store.py`

当前名称叫 `ChromaStore`，但 MVP 阶段实际实现是本地 JSON 向量存储：

- 持久化位置：`data/vector_db/chroma/chunks.json`。
- `add_chunks`：写入一批 chunk 向量。
- `search`：按 cosine similarity 返回 Top K。
- `delete_document`：删除指定 document_id 的旧向量记录。

注意：当前还不是真实 Chroma 服务或 ChromaDB 客户端。

### `RetrievalService`

文件位置：`backend/app/services/retrieval_service.py`

负责检索：

1. 对 query 调用 `EmbeddingService.embed_text`。
2. 调用 `ChromaStore.search`。
3. 返回 `RetrievalSearchResponse`。

这里不调用大模型，只负责“找资料”。

### `LLMService`

文件位置：`backend/app/services/llm_service.py`

负责统一封装 OpenAI-compatible chat completion：

- 从 `.env` 读取 `LLM_PROVIDER`、`LLM_BASE_URL`、`LLM_API_KEY`、`LLM_MODEL`。
- 支持 `siliconflow`、`deepseek`、`openai_compatible`。
- 对外提供 `generate_chat_completion(messages)`。

业务代码不直接依赖具体模型厂商。

### `RagService`

文件位置：`backend/app/services/rag_service.py`

负责 RAG 问答：

1. 调用 `RetrievalService.search` 获取 Top K chunks。
2. 将 chunk 内容拼成 context。
3. 读取 `backend/app/prompts/repair_qa_prompt.txt`。
4. 调用 `LLMService`。
5. 优先解析 JSON 输出；失败时按 Markdown 宽松解析；再失败则保留原始回答到 `answer`。
6. sources 始终来自检索结果，不由模型生成。

稳定性处理：

- 检索向量化失败时返回结构化 fallback，不直接 500。
- LLM 调用失败时返回结构化 fallback。

### `WorkOrderService`

文件位置：`backend/app/services/workorder_service.py`

负责检修记录：

- `create_workorder`：保存 RAG 输出和 sources。
- `list_workorders`：按创建时间倒序返回记录列表。
- `get_workorder`：按 `work_order_id` 查看详情。

注意：当前 WorkOrder 是“把一次问答结果沉淀为记录”，还没有审批流、状态流转、权限、编辑历史。

## 3. 核心 API 输入输出

### `GET /health`

用途：后端健康检查。

响应：

```json
{
  "status": "ok"
}
```

### `GET /api/documents`

用途：查看文档列表和处理状态。

响应核心字段：

```json
{
  "items": [
    {
      "document_id": "doc-xxxx",
      "filename": "manual.md",
      "file_path": "data/uploads/doc-xxxx_manual.md",
      "file_type": "markdown",
      "status": "indexed",
      "upload_time": "2026-..."
    }
  ]
}
```

### `POST /api/documents/upload`

用途：上传 PDF、TXT、Markdown。

输入：`multipart/form-data`，字段名为 `file`。

响应核心字段：

```json
{
  "document_id": "doc-xxxx",
  "filename": "manual.md",
  "file_type": "markdown",
  "status": "uploaded",
  "message": "文档上传成功，当前状态为 uploaded。"
}
```

### `POST /api/documents/{document_id}/parse`

用途：将文档解析为纯文本。

输入：路径参数 `document_id`。

响应核心字段：

```json
{
  "document_id": "doc-xxxx",
  "status": "parsed",
  "message": "文档解析完成。",
  "output_path": "data/parsed/documents/doc-xxxx.txt"
}
```

### `POST /api/documents/{document_id}/chunk`

用途：将解析后的文本切成 chunks，并写入 SQLite。

响应核心字段：

```json
{
  "document_id": "doc-xxxx",
  "status": "chunked",
  "message": "文本切分完成，切片已写入 SQLite。",
  "chunk_count": 5
}
```

### `POST /api/documents/{document_id}/index`

用途：将 chunks 向量化并写入本地向量存储。

响应核心字段：

```json
{
  "document_id": "doc-xxxx",
  "status": "indexed",
  "message": "文档向量入库完成。",
  "chunk_count": 5
}
```

### `POST /api/retrieval/search`

用途：只做检索，不调用大模型。

请求：

```json
{
  "query": "设备启动后电源指示灯不亮，风扇也不转，应该如何排查？",
  "top_k": 5
}
```

响应核心字段：

```json
{
  "query": "...",
  "results": [
    {
      "chunk_id": "chk-xxxx",
      "document_id": "doc-xxxx",
      "document_title": "manual.md",
      "chunk_text": "...",
      "score": 0.78,
      "metadata": {
        "filename": "manual.md",
        "file_type": "markdown",
        "chunk_index": 0,
        "start_offset": 0,
        "end_offset": 700
      }
    }
  ]
}
```

### `POST /api/chat/repair`

用途：RAG 检修问答。

请求：

```json
{
  "question": "设备运行 10 分钟后自动断电，可能是什么原因？",
  "equipment_type": "电源模块",
  "top_k": 5
}
```

响应核心字段：

```json
{
  "answer": "",
  "fault_understanding": "...",
  "possible_causes": ["..."],
  "repair_steps": ["..."],
  "safety_notes": ["..."],
  "sources": [
    {
      "chunk_id": "chk-xxxx",
      "document_id": "doc-xxxx",
      "document_title": "manual.md",
      "filename": "manual.md",
      "chunk_index": 0,
      "score": 0.78,
      "metadata": {}
    }
  ]
}
```

说明：`sources` 由系统从检索结果生成，不由模型生成。

### `POST /api/workorders/create`

用途：将一次 RAG 回答保存为检修记录。

请求核心字段：

```json
{
  "equipment_type": "电源模块",
  "fault_symptom": "设备启动后电源指示灯不亮，风扇也不转",
  "fault_understanding": "...",
  "possible_causes": ["..."],
  "repair_steps": ["..."],
  "safety_notes": ["..."],
  "sources": [],
  "operator_note": ""
}
```

响应核心字段：

```json
{
  "work_order_id": "wo-xxxx",
  "status": "created",
  "created_at": "2026-..."
}
```

### `GET /api/workorders`

用途：查看检修记录列表。

响应：

```json
{
  "items": [
    {
      "work_order_id": "wo-xxxx",
      "fault_symptom": "...",
      "status": "created",
      "created_at": "2026-..."
    }
  ]
}
```

### `GET /api/workorders/{work_order_id}`

用途：查看检修记录详情。

响应结构与 `WorkOrderItem` 一致，包含故障现象、RAG 输出、sources、状态和创建时间。

## 4. 核心对象关系

### Document

代表一份上传资料。保存在 `documents` 表。

关键字段：

- `document_id`
- `filename`
- `file_path`
- `file_type`
- `status`
- `parsed_text_path`
- `error_message`

状态流转：

```text
uploaded -> parsed -> chunked -> indexed
失败时 -> failed
```

### Chunk

代表从文档解析文本中切出来的一段知识片段。保存在 `chunks` 表。

关键字段：

- `chunk_id`
- `document_id`
- `chunk_text`
- `chunk_index`
- `metadata_json`

关系：一个 Document 可以有多个 Chunk。

### Source

代表 RAG 回答引用的依据来源。

来源不是模型生成的，而是由检索结果转换得到。

关键字段：

- `chunk_id`
- `document_id`
- `document_title`
- `filename`
- `chunk_index`
- `score`
- `metadata`

关系：Source 指向某个 Chunk，并保留检索相似度和元数据。

### RAGAnswer

当前没有单独建表，表现为 `/api/chat/repair` 的响应。

核心字段：

- `fault_understanding`
- `possible_causes`
- `repair_steps`
- `safety_notes`
- `sources`
- `answer`

关系：RAGAnswer 使用 Source 作为依据，并可被保存为 WorkOrder。

### WorkOrder

代表一次沉淀下来的检修记录。保存在 `workorders` 表。

关键字段：

- `work_order_id`
- `equipment_type`
- `fault_symptom`
- `fault_understanding`
- `possible_causes_json`
- `repair_steps_json`
- `safety_notes_json`
- `sources_json`
- `operator_note`
- `status`
- `created_at`

关系：WorkOrder 保存 RAGAnswer 的结构化内容和完整 sources，用于事后追溯。

## 5. 常见问题定位表

| 现象 | 优先检查 | 可能原因 | 处理建议 |
| --- | --- | --- | --- |
| 前端无法访问接口 | 后端是否启动、`VITE_API_BASE_URL` | 后端未运行、端口不对、CORS 地址不匹配 | 启动 FastAPI，确认前端指向 `http://127.0.0.1:8000/api` |
| 上传失败 | 文件后缀、接口报错 | 只支持 PDF/TXT/MD/Markdown | 换成支持格式，检查文件名是否为空 |
| parse 失败 | `documents.status`、`error_message`、原始文件是否存在 | 文件丢失、PDF 是扫描件、编码不支持 | 重新上传，或先转换成可复制文本的 PDF/TXT/MD |
| chunk 失败 | `parsed_text_path` 是否存在 | 文档未解析、解析结果为空 | 先 parse，再 chunk；检查解析后的 txt 是否有内容 |
| index 失败 | `.env` embedding 配置、`error_message` | API key、base_url、model 错误或网络超时 | 检查 `EMBEDDING_PROVIDER/BASE_URL/API_KEY/MODEL` |
| search 返回空 | `data/vector_db/chroma/chunks.json` | 还没 index，或向量库被清空 | 对文档重新执行 index |
| search 分数全 0 | embedding 维度不一致或旧索引残留 | 旧 mock 索引和真实 embedding 混用 | 清理向量库后重新 index |
| RAG 返回“知识库中未找到充分依据” | search 结果是否相关 | 检索不到相关资料、LLM 调用失败、资料域不匹配 | 先跑 `scripts/test_retrieval.py` 看 Top K，再跑 RAG |
| sources 缺失 | RAG 返回结果 | 检索失败或向量化失败 | 检查 retrieval/search 是否正常 |
| WorkOrder 没有来源 | 创建请求中的 `sources` | 前端保存时 RAG 结果没有 sources | 先确认 RAG 页面结果区有依据来源 |
| 文档状态变成 failed | `documents.error_message` | parse/chunk/index 任一环节失败 | 根据 error_message 定位具体阶段 |

## 6. 当前技术债列表

### 需要优先处理

- `ChromaStore` 目前是本地 JSON 存储，不是真实 Chroma；并发写入时稳定性有限。
- chunk 仍是固定长度切分，不理解标题、章节、表格和案例边界。
- `equipment_type` 当前只进入 RAG prompt，没有参与检索过滤。
- WorkOrder 当前信任前端提交的 RAG 输出，后续如果强调可信审计，应由服务端固化一次 RAG 结果再生成记录。

### 可以后续优化

- PDF 解析不支持 OCR，扫描件无法处理。
- RAG prompt 仍偏检修问答场景，后续泛化到工程文档时应抽象为可配置 prompt。
- `common_schema.SourceItem` 与 `chat_schema.SourceItem` 存在概念重叠，后续可统一。
- 向量存储缺少按 `document_id`、`source_type`、`equipment_type` 的过滤检索能力。
- 前端没有登录、权限、角色和审计。
- WorkOrder 还没有编辑、关闭、审批、导出等状态流转。
- 缺少自动化 API 集成测试，目前主要依赖脚本和人工验证。

## 7. 负责人视角的判断

当前系统已经不是单纯“上传文件”的 demo，而是具备了一个可演示的 RAG 作业闭环：

```text
资料进入知识库 -> 检索出依据 -> 模型基于依据回答 -> 一键生成检修记录
```

当前最重要的质量判断点不是页面是否漂亮，而是：

- 检索结果是否命中正确资料。
- RAG 回答是否严格基于 sources。
- WorkOrder 是否完整保存 sources。
- 失败时是否能快速定位到 parse、chunk、index、search、LLM 哪个环节。

