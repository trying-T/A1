# 系统架构说明

## 1. 架构目标

系统架构围绕比赛主链路设计，要求实现简单、便于演示、易于后续扩展。核心原则是分层清晰，不把所有业务逻辑堆在单个接口文件中。

## 2. 总体分层

### 2.1 资料层

位于 `data/uploads/`，保存原始资料，包括：

- `manuals/`：设备手册
- `fault_cases/`：故障案例
- `sop/`：标准作业流程
- `safety_rules/`：安全规范

### 2.2 解析与索引层

主要由后端 `services` 和 `vectorstore` 实现：

- `parser_service`：解析原始文档
- `chunk_service`：切分文本片段
- `embedding_service`：调用向量化能力
- `retrieval_service`：检索相关知识
- `vectorstore/chroma_store`：封装向量库访问

### 2.3 生成层

- `rag_service`：组织 RAG 问答流程
- `llm_service`：统一封装模型调用
- `prompts/`：控制输出结构与回答风格

### 2.4 业务层

- `document_service`：文档状态和处理流转
- `workorder_service`：检修记录生成与查询

### 2.5 展示层

前端页面聚焦三个核心场景：

- 知识库管理
- 检修问答
- 检修记录

## 3. 核心数据流

1. 用户上传维修资料。
2. 系统解析资料并切分知识片段。
3. 系统建立向量索引。
4. 用户输入检修问题。
5. 系统检索相关知识片段。
6. 大模型基于检索结果生成结构化回答。
7. 系统将回答结果保存为检修记录。

## 4. 目录映射

### 4.1 后端

- `backend/app/api/`：接口层
- `backend/app/services/`：业务逻辑层
- `backend/app/schemas/`：输入输出结构
- `backend/app/models/`：数据模型
- `backend/app/prompts/`：提示词模板
- `backend/app/vectorstore/`：向量库封装

### 4.2 前端

- `frontend/src/pages/`：页面
- `frontend/src/components/`：组件
- `frontend/src/api/`：接口调用
- `frontend/src/types/`：前端类型定义

## 5. 扩展设计

后续若需要增加图片识别、多模态理解、Agent 调度或知识图谱，可以在现有结构上扩展对应模块，而不需要推翻当前主链路：

- `backend/app/multimodal/`
- `backend/app/agents/`
- `backend/app/graph/`

这种做法可以确保 MVP 阶段的系统足够轻，同时保留未来演进空间。
