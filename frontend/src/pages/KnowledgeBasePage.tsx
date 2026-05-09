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
    await runDocumentAction(documentId, "parse", () => parseDocument(documentId));
  }

  async function handleChunk(documentId: string) {
    await runDocumentAction(documentId, "chunk", () => chunkDocument(documentId));
  }

  async function handleIndex(documentId: string) {
    await runDocumentAction(documentId, "index", () => indexDocument(documentId));
  }

  async function runDocumentAction(
    documentId: string,
    type: ActionState["type"],
    action: () => Promise<{ message: string; chunk_count?: number | null }>,
  ) {
    setActionState({ loading: true, targetId: documentId, type });
    setError("");
    try {
      const result = await action();
      const suffix = result.chunk_count ? ` 共处理 ${result.chunk_count} 个片段。` : "";
      setMessage(`${result.message}${suffix}`);
      await refreshDocuments();
    } catch (nextError) {
      setError(getErrorMessage(nextError));
    } finally {
      setActionState({ loading: false, targetId: null, type: null });
    }
  }

  const indexedCount = documents.filter((item) => item.status === "indexed").length;
  const chunkedCount = documents.filter((item) => item.status === "chunked").length;

  return (
    <div className="page-stack">
      <section className="metric-grid">
        <MetricCard label="文档总数" value={documents.length} hint="SQLite documents" />
        <MetricCard label="已切分" value={chunkedCount} hint="可继续向量入库" />
        <MetricCard label="已入库" value={indexedCount} hint="可参与 RAG 检索" />
      </section>

      <section className="pro-card upload-card">
        <div>
          <p className="section-eyebrow">Knowledge Ingestion</p>
          <h2>上传检修资料</h2>
          <p>文件会保存到 <code>data/uploads</code>，初始状态为 <code>uploaded</code>。</p>
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
            <span>{selectedFile ? selectedFile.name : "选择 PDF / TXT / Markdown"}</span>
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

      <section className="pro-card">
        <div className="card-header">
          <div>
            <p className="section-eyebrow">Document Pipeline</p>
            <h2>文档处理状态</h2>
          </div>
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
    </div>
  );
}

function MetricCard({ label, value, hint }: { label: string; value: number; hint: string }) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{hint}</small>
    </article>
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
