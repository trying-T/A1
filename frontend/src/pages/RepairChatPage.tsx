import { FormEvent, useState } from "react";

import { repairChat } from "../api/chatApi";
import type { RepairChatResponse } from "../types/repairChat";

const DEFAULT_QUESTION = "设备启动后电源指示灯不亮，风扇也不转，应该如何排查？";

export default function RepairChatPage() {
  const [question, setQuestion] = useState(DEFAULT_QUESTION);
  const [equipmentType, setEquipmentType] = useState("");
  const [result, setResult] = useState<RepairChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!question.trim()) {
      setError("请先输入故障问题。");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const response = await repairChat({
        question: question.trim(),
        equipment_type: equipmentType.trim() || null,
        top_k: 5,
      });
      setResult(response);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "RAG 问答请求失败，请稍后重试。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-stack">
      <section className="pro-card chat-compose-card">
        <div>
          <p className="section-eyebrow">Repair Assistant</p>
          <h2>生成检修建议</h2>
          <p>系统会先检索知识库，再让模型基于参考片段生成结构化回答。</p>
        </div>

        <form className="chat-form" onSubmit={(event) => void handleSubmit(event)}>
          <label className="field-label">
            <span>故障问题</span>
            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="例如：设备启动后电源指示灯不亮，风扇也不转，应该如何排查？"
              rows={5}
            />
          </label>

          <label className="field-label">
            <span>设备类型（可选）</span>
            <input
              value={equipmentType}
              onChange={(event) => setEquipmentType(event.target.value)}
              placeholder="例如：电源模块、控制柜、空压机"
            />
          </label>

          <div className="chat-actions">
            <button className="primary-button" type="submit" disabled={loading}>
              {loading ? "生成中..." : "生成检修建议"}
            </button>
            <button
              className="secondary-button"
              type="button"
              disabled={loading}
              onClick={() => {
                setQuestion("");
                setEquipmentType("");
                setResult(null);
                setError("");
              }}
            >
              清空
            </button>
          </div>
        </form>
      </section>

      {error ? <div className="feedback error">{error}</div> : null}

      {result ? (
        <section className="answer-layout">
          <div className="answer-main">
            <ResultSection title="故障理解" items={[result.fault_understanding]} />
            <ResultSection title="可能原因" items={result.possible_causes} ordered />
            <ResultSection title="排查步骤" items={result.repair_steps} ordered />
            <ResultSection title="安全注意事项" items={result.safety_notes} />

            {result.answer ? (
              <details className="pro-card raw-answer">
                <summary>查看原始模型回答</summary>
                <pre>{result.answer}</pre>
              </details>
            ) : null}
          </div>

          <aside className="source-panel pro-card">
            <div className="card-header compact">
              <div>
                <p className="section-eyebrow">Sources</p>
                <h2>依据来源</h2>
              </div>
              <span className="source-count">{result.sources.length}</span>
            </div>
            {result.sources.length === 0 ? (
              <div className="empty-state">没有检索到可追溯来源。</div>
            ) : (
              <div className="source-list">
                {result.sources.map((source) => (
                  <article className="source-card" key={`${source.document_id}-${source.chunk_id}`}>
                    <strong>{source.filename ?? source.document_title}</strong>
                    <span>score: {source.score.toFixed(4)}</span>
                    <small>chunk_id: {source.chunk_id}</small>
                    <small>document_id: {source.document_id}</small>
                    {source.chunk_index !== null && source.chunk_index !== undefined ? (
                      <small>chunk_index: {source.chunk_index}</small>
                    ) : null}
                  </article>
                ))}
              </div>
            )}
          </aside>
        </section>
      ) : (
        <div className="empty-state">
          先输入一个故障问题。建议先用脚本验证 RAG 质量，再在这里进行交互演示。
        </div>
      )}
    </div>
  );
}

function ResultSection({
  title,
  items,
  ordered = false,
}: {
  title: string;
  items: string[];
  ordered?: boolean;
}) {
  const normalizedItems = items.filter(Boolean);
  const ListTag = ordered ? "ol" : "ul";
  return (
    <section className="pro-card result-section">
      <h2>{title}</h2>
      {normalizedItems.length === 0 ? (
        <p className="muted">暂无结构化内容。</p>
      ) : (
        <ListTag>
          {normalizedItems.map((item, index) => (
            <li key={`${title}-${index}`}>{item}</li>
          ))}
        </ListTag>
      )}
    </section>
  );
}
