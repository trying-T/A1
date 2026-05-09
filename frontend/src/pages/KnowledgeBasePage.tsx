import { ChangeEvent, useEffect, useState } from "react";

import {
  chunkDocument,
  getDocuments,
  indexDocument,
  parseDocument,
  uploadDocument,
} from "../api/documentApi";
import type { DocumentItem } from "../types/document";

type ActionState = {
  loading: boolean;
  targetId: string | null;
  type: "upload" | "parse" | "chunk" | "index" | null;
};

const statusLabelMap: Record<string, string> = {
  uploaded: "已上传",
  parsed: "已解析",
  chunked: "已切分",
  indexed: "已入库",
};

export default function KnowledgeBasePage() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pageLoading, setPageLoading] = useState(true);
  const [message, setMessage] = useState("正在加载文档列表...");
  const [error, setError] = useState("");
  const [actionState, setActionState] = useState<ActionState>({
    loading: false,
    targetId: null,
    type: null,
  });

  useEffect(() => {
    void refreshDocuments();
  }, []);

  async function refreshDocuments() {
    setPageLoading(true);
    setError("");
    try {
      const result = await getDocuments();
      setDocuments(result.items);
      setMessage(result.items.length > 0 ? "文档列表已更新。" : "当前还没有已上传文档。");
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setPageLoading(false);
    }
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    setSelectedFile(event.target.files?.[0] ?? null);
    setError("");
  }

  async function handleUpload() {
    if (!selectedFile) {
      setError("请先选择一个 PDF、TXT 或 Markdown 文件。");
      return;
    }

    setActionState({ loading: true, targetId: null, type: "upload" });
    setError("");
    try {
      const result = await uploadDocument(selectedFile);
      setMessage(result.message);
      setSelectedFile(null);
      await refreshDocuments();
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setActionState({ loading: false, targetId: null, type: null });
      const input = document.getElementById("upload-input") as HTMLInputElement | null;
      if (input) {
        input.value = "";
      }
    }
  }

  async function handleParse(documentId: string) {
    setActionState({ loading: true, targetId: documentId, type: "parse" });
    setError("");
    try {
      const result = await parseDocument(documentId);
      setMessage(result.message);
      await refreshDocuments();
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setActionState({ loading: false, targetId: null, type: null });
    }
  }

  async function handleChunk(documentId: string) {
    setActionState({ loading: true, targetId: documentId, type: "chunk" });
    setError("");
    try {
      const result = await chunkDocument(documentId);
      const suffix = result.chunk_count ? ` 共写入 ${result.chunk_count} 个片段。` : "";
      setMessage(`${result.message}${suffix}`);
      await refreshDocuments();
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setActionState({ loading: false, targetId: null, type: null });
    }
  }

  async function handleIndex(documentId: string) {
    setActionState({ loading: true, targetId: documentId, type: "index" });
    setError("");
    try {
      const result = await indexDocument(documentId);
      const suffix = result.chunk_count ? ` 共入库 ${result.chunk_count} 个片段。` : "";
      setMessage(`${result.message}${suffix}`);
      await refreshDocuments();
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setActionState({ loading: false, targetId: null, type: null });
    }
  }

  return (
    <main className="app-shell">
      <section className="knowledge-shell">
        <header className="knowledge-header">
          <div>
            <p className="eyebrow">Stage 1 · Knowledge Ingestion</p>
            <h1>知识库管理</h1>
            <p className="lead">
              当前阶段只聚焦最小闭环：上传文档、解析纯文本、切分知识片段，并把处理状态稳定展示出来。
            </p>
          </div>
          <div className="hint-panel">
            <span>支持格式</span>
            <strong>PDF / TXT / Markdown</strong>
            <small>建议优先使用文本型 PDF，扫描件可能无法直接提取文字。</small>
          </div>
        </header>

        <section className="upload-panel">
          <div className="upload-copy">
            <h2>上传文档</h2>
            <p>
              文件会保存到 <code>data/uploads</code>，初始状态为 <code>uploaded</code>。
            </p>
          </div>
          <div className="upload-controls">
            <label className="file-picker" htmlFor="upload-input">
              <input
                id="upload-input"
                type="file"
                accept=".pdf,.txt,.md,.markdown"
                onChange={handleFileChange}
                disabled={actionState.loading}
              />
              <span>{selectedFile ? selectedFile.name : "选择文件"}</span>
            </label>
            <button
              className="primary-button"
              type="button"
              onClick={() => void handleUpload()}
              disabled={actionState.loading}
            >
              {actionState.loading && actionState.type === "upload" ? "上传中..." : "上传文档"}
            </button>
          </div>
        </section>

        {error ? <div className="feedback error">{error}</div> : null}
        {!error && message ? <div className="feedback success">{message}</div> : null}

        <section className="table-panel">
          <div className="table-header">
            <h2>文档列表</h2>
            <button className="ghost-button" type="button" onClick={() => void refreshDocuments()}>
              刷新列表
            </button>
          </div>

          {pageLoading ? (
            <div className="empty-state">正在读取数据库中的文档记录...</div>
          ) : documents.length === 0 ? (
            <div className="empty-state">还没有文档，先上传一份检修资料试试。</div>
          ) : (
            <div className="table-wrap">
              <table className="document-table">
                <thead>
                  <tr>
                    <th>文件名</th>
                    <th>类型</th>
                    <th>上传时间</th>
                    <th>状态</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((item) => {
                    const isBusy = actionState.loading && actionState.targetId === item.document_id;
                    return (
                      <tr key={item.document_id}>
                        <td>
                          <div className="file-cell">
                            <strong>{item.filename}</strong>
                            <small>{item.document_id}</small>
                          </div>
                        </td>
                        <td>{item.file_type}</td>
                        <td>{formatDate(item.upload_time)}</td>
                        <td>
                          <span className={`status-pill status-${item.status}`}>
                            {statusLabelMap[item.status] ?? item.status}
                          </span>
                        </td>
                        <td>
                          <div className="table-actions">
                            <button
                              className="secondary-button"
                              type="button"
                              onClick={() => void handleParse(item.document_id)}
                              disabled={actionState.loading}
                            >
                              {isBusy && actionState.type === "parse" ? "解析中..." : "解析"}
                            </button>
                            <button
                              className="secondary-button"
                              type="button"
                              onClick={() => void handleChunk(item.document_id)}
                              disabled={actionState.loading || item.status === "uploaded"}
                            >
                              {isBusy && actionState.type === "chunk" ? "切分中..." : "切分"}
                            </button>
                            <button
                              className="secondary-button"
                              type="button"
                              onClick={() => void handleIndex(item.document_id)}
                              disabled={
                                actionState.loading ||
                                item.status === "uploaded" ||
                                item.status === "parsed"
                              }
                            >
                              {isBusy && actionState.type === "index" ? "入库中..." : "入库"}
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

function formatDate(value: string) {
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }
  return parsed.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "操作失败，请稍后重试。";
}
