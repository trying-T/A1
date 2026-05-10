# API 调用流程追踪

本文用流程追踪的方式说明当前系统从前端点击到后端服务、数据库、向量存储和模型调用之间的实际路径。它不是接口宣传文档，而是用于理解系统和定位问题的运行手册。

## 1. 文档入库流程

文档入库包括四步：

```text
upload -> parse -> chunk -> index
```

### 1.1 上传文档

前端入口：

```text
KnowledgeBasePage -> uploadDocument(file)
```

接口：

```text
POST /api/documents/upload
```

后端调用链：

```text
documents.py
-> DocumentService.save_upload
-> data/uploads
-> documents 表
```

关键动作：

1. 校验文件名。
2. 校验后缀是否为 `.pdf`、`.txt`、`.md`、`.markdown`。
3. 生成 `document_id`。
4. 文件保存到 `data/uploads`。
5. `documents` 表插入一条记录。
6. 状态设为 `uploaded`。

成功后，系统只知道“文件已经上传”，还没有任何可检索知识。

### 1.2 解析文档

前端入口：

```text
KnowledgeBasePage -> parseDocument(documentId)
```

接口：

```text
POST /api/documents/{document_id}/parse
```

后端调用链：

```text
documents.py
-> DocumentService.parse_document
-> ParserService.parse_file
-> data/parsed/documents/{document_id}.txt
-> documents 表
```

关键动作：

1. 根据 `document_id` 查 `documents` 表。
2. 解析前清理旧 chunks 和旧 vector records。
3. 找到原始文件 `file_path`。
4. 调用 `ParserService`：
   - PDF 使用 `pypdf`。
   - TXT/Markdown 使用多编码尝试读取。
5. 将解析结果写入 `data/parsed/documents/{document_id}.txt`。
6. 更新 `documents.status = parsed`。
7. 更新 `documents.parsed_text_path`。
8. 清空 `error_message`。

失败处理：

```text
documents.status = failed
documents.error_message = 失败原因
```

注意：parse 后不会自动 chunk，也不会自动 index。

### 1.3 切分文档

前端入口：

```text
KnowledgeBasePage -> chunkDocument(documentId)
```

接口：

```text
POST /api/documents/{document_id}/chunk
```

后端调用链：

```text
documents.py
-> DocumentService.chunk_document
-> ChunkService.split_text
-> chunks 表
-> documents 表
```

关键动作：

1. 根据 `document_id` 查 `documents` 表。
2. 切分前清理该文档旧 chunks 和旧 vector records。
3. 读取 `parsed_text_path`。
4. 调用 `ChunkService.split_text`。
5. 将每个 chunk 写入 `chunks` 表。
6. 每个 chunk 保存：
   - `chunk_id`
   - `document_id`
   - `chunk_text`
   - `chunk_index`
   - `metadata_json`
7. 更新 `documents.status = chunked`。
8. 清空 `error_message`。

当前切分规则：

```text
chunk_size = 700
overlap = 100
```

也就是每段大约 700 字，相邻片段重叠 100 字。

失败处理：

```text
documents.status = failed
documents.error_message = 失败原因
```

### 1.4 向量入库

前端入口：

```text
KnowledgeBasePage -> indexDocument(documentId)
```

接口：

```text
POST /api/documents/{document_id}/index
```

后端调用链：

```text
documents.py
-> DocumentService.index_document
-> EmbeddingService.embed_texts
-> ChromaStore.add_chunks
-> data/vector_db/chroma/chunks.json
-> documents 表
```

关键动作：

1. 根据 `document_id` 查 `documents` 表。
2. index 前先删除该文档旧 vector records。
3. 从 `chunks` 表读取当前 chunks。
4. 调用 `EmbeddingService.embed_texts`。
5. 为每个 chunk 组装向量记录：
   - `chunk_id`
   - `document_id`
   - `chunk_text`
   - `embedding`
   - `metadata`
6. 写入 `data/vector_db/chroma/chunks.json`。
7. 更新 `documents.status = indexed`。
8. 清空 `error_message`。

失败处理：

```text
documents.status = failed
documents.error_message = 失败原因
```

如果 embedding provider 配置错误，会返回明确错误，不会自动退回 mock。

## 2. 检索流程

检索流程只负责找相关 chunk，不调用大模型。

前端或脚本入口：

```text
scripts/test_retrieval.py
或
POST /api/retrieval/search
```

接口：

```text
POST /api/retrieval/search
```

请求：

```json
{
  "query": "报警代码 E07 可能代表什么？",
  "top_k": 5
}
```

后端调用链：

```text
retrieval.py
-> RetrievalService.search
-> EmbeddingService.embed_text
-> ChromaStore.search
-> RetrievalSearchResponse
```

执行过程：

1. 接收用户 query。
2. 调用 `EmbeddingService.embed_text` 得到 query 向量。
3. 读取本地向量存储 `chunks.json`。
4. 对 query 向量和每个 chunk 向量计算 cosine similarity。
5. 按 score 倒序排序。
6. 返回 Top K。

响应中的每个结果包括：

```text
chunk_id
document_id
document_title
chunk_text
score
metadata
```

异常处理：

- embedding 失败时，`/api/retrieval/search` 返回 502。
- 错误信息包含 provider/model，方便检查 `.env`。
- 不暴露 API key。

定位建议：

如果 RAG 回答质量差，先不要看大模型，先看 `/api/retrieval/search` 的 Top K 是否相关。

## 3. RAG 问答流程

RAG 问答是在检索基础上调用大模型。

前端入口：

```text
RepairChatPage -> repairChat(payload)
```

接口：

```text
POST /api/chat/repair
```

请求：

```json
{
  "question": "设备运行 10 分钟后自动断电，可能是什么原因？",
  "equipment_type": "电源模块",
  "top_k": 5
}
```

后端调用链：

```text
chat.py
-> RagService.answer
-> RagService.answer_repair
-> RetrievalService.search
-> RagService._build_context
-> repair_qa_prompt.txt
-> LLMService.generate_chat_completion
-> RagService._parse_model_output
-> RepairChatResponse
```

执行过程：

1. 接收 `question`、`equipment_type`、`top_k`。
2. 调用检索服务拿 Top K chunks。
3. 将检索结果转换为 sources。
4. 将 chunks 拼接为 context。
5. 读取 `backend/app/prompts/repair_qa_prompt.txt`。
6. 组装 messages：
   - system：系统 prompt。
   - user：设备类型、用户问题、参考资料。
7. 调用 LLM。
8. 优先解析模型返回 JSON。
9. 如果不是合法 JSON，则按 Markdown 标题宽松解析。
10. 如果仍解析失败，将原始回答保留到 `answer`。
11. 返回结构化结果。

返回内容：

```text
fault_understanding
possible_causes
repair_steps
safety_notes
sources
answer
```

关键约束：

- sources 不由模型生成。
- sources 来自检索结果。
- 模型只能基于参考资料回答。
- 资料不足时应说明“知识库中未找到充分依据”。

异常处理：

### 检索或 embedding 失败

如果 query 向量化失败：

```text
RagService 返回结构化 fallback
sources = []
不会直接 500
```

### LLM 调用失败

如果 LLM provider、base_url、api_key、model 配置错误，或网络失败：

```text
RagService 返回结构化 fallback
sources 仍保留检索结果
```

这样做的目的是：即使模型失败，项目负责人仍能看到检索依据是否正确。

## 4. 检修记录生成流程

检修记录生成不是重新问模型，而是把当前 RAG 结果保存下来。

前端入口：

```text
RepairChatPage -> 生成检修记录按钮
```

接口：

```text
POST /api/workorders/create
```

前端调用链：

```text
RepairChatPage
-> createWorkOrder(payload)
-> POST /api/workorders/create
-> 成功后切换到 WorkOrderPage
-> WorkOrderPage 默认定位新记录
```

后端调用链：

```text
workorders.py
-> WorkOrderService.create_workorder
-> workorders 表
-> WorkOrderItem
```

保存内容：

```text
equipment_type
fault_symptom
fault_understanding
possible_causes
repair_steps
safety_notes
sources
operator_note
status
created_at
```

其中：

- `fault_symptom` 来自用户问题。
- `fault_understanding`、`possible_causes`、`repair_steps`、`safety_notes` 来自 RAG 输出。
- `sources` 来自 RAG 响应里的检索来源。
- `status` 当前固定为 `created`。

成功后：

```text
返回 work_order_id
前端跳转到检修记录页面
检修记录页面优先选中新生成的记录
```

## 5. 四条主流程的排查顺序

### 5.1 文档入库失败

排查顺序：

```text
documents 表 status/error_message
-> data/uploads 是否有原始文件
-> data/parsed/documents 是否有解析文本
-> chunks 表是否有对应 document_id
-> data/vector_db/chroma/chunks.json 是否有对应 document_id
```

### 5.2 检索结果不相关

排查顺序：

```text
是否上传了相关领域资料
-> 是否 parse/chunk/index 都成功
-> 是否混用了 mock 和真实 embedding 旧索引
-> scripts/test_retrieval.py 的 Top K 是否合理
-> chunk 是否过大导致多个案例混在一起
```

### 5.3 RAG 回答不可靠

排查顺序：

```text
先看 retrieval/search 是否命中
-> 再看 sources 是否正确
-> 再看 prompt 是否限制模型基于资料回答
-> 最后看 LLM 模型输出是否是合法 JSON
```

如果 search 都不相关，不应该先调 prompt，而应该先处理资料、embedding 或 chunk。

### 5.4 WorkOrder 来源丢失

排查顺序：

```text
RepairChatPage 是否展示 sources
-> /api/chat/repair 响应 sources 是否为空
-> /api/workorders/create 请求 payload 是否包含 sources
-> workorders.sources_json 是否保存完整
```

## 6. 当前数据存储位置

| 数据 | 位置 |
| --- | --- |
| 原始上传文件 | `data/uploads` |
| 解析后纯文本 | `data/parsed/documents` |
| SQLite 数据库 | `data/sqlite/app.db` |
| documents 表 | SQLite |
| chunks 表 | SQLite |
| workorders 表 | SQLite |
| 本地向量记录 | `data/vector_db/chroma/chunks.json` |
| RAG prompt | `backend/app/prompts/repair_qa_prompt.txt` |
| 检索测试报告 | `data/demo/retrieval_test_report.md` |
| RAG 测试报告 | `data/demo/rag_chat_test_report.md` |

## 7. 当前接口边界

当前系统的接口边界是稳定的：

```text
documents 接口负责资料处理
retrieval 接口负责检索
chat 接口负责 RAG 回答
workorders 接口负责记录沉淀
```

这几个边界不要轻易混在一起。例如：

- 不要让 upload 自动调用 RAG。
- 不要让 search 调用 LLM。
- 不要让 LLM 生成 sources。
- 不要让 WorkOrder 重新检索或重新生成回答。

保持这个边界，系统以后扩展真实 Chroma、章节切分、权限、审批流时会更稳。

## 8. 项目负责人应关注的验收点

当前阶段验收不应只看接口是否 200，而应看：

1. 文档状态是否按 `uploaded -> parsed -> chunked -> indexed` 流转。
2. 失败时是否进入 `failed`，并有 `error_message`。
3. 检索 Top K 是否来自正确文档。
4. RAG 回答是否引用了正确 sources。
5. WorkOrder 是否完整保存 sources。
6. 重新 parse/chunk/index 后，旧 chunk 是否不再出现在 search 结果中。

如果这些都成立，说明系统已经具备可解释、可追溯、可继续扩展的基础。

