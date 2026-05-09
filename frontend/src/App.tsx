import { useState } from "react";

import KnowledgeBasePage from "./pages/KnowledgeBasePage";
import RepairChatPage from "./pages/RepairChatPage";

type ActivePage = "knowledge" | "repair";

const menuItems: Array<{
  key: ActivePage;
  label: string;
  description: string;
  icon: string;
}> = [
  {
    key: "knowledge",
    label: "知识库",
    description: "上传、解析、切分、入库",
    icon: "KB",
  },
  {
    key: "repair",
    label: "检修问答",
    description: "RAG 建议与来源追溯",
    icon: "AI",
  },
];

const pageMeta: Record<ActivePage, { title: string; subtitle: string }> = {
  knowledge: {
    title: "知识库管理",
    subtitle: "维护检修资料入库链路，确保检索前的资料状态稳定可见。",
  },
  repair: {
    title: "检修问答",
    subtitle: "基于知识库片段生成结构化检修建议，保留可追溯 sources。",
  },
};

export default function App() {
  const [activePage, setActivePage] = useState<ActivePage>("knowledge");
  const current = pageMeta[activePage];

  return (
    <div className="pro-shell">
      <aside className="pro-sider">
        <div className="brand-block">
          <div className="brand-mark">A1</div>
          <div>
            <strong>Repair RAG</strong>
            <span>设备检修知识系统</span>
          </div>
        </div>

        <nav className="pro-menu" aria-label="主导航">
          {menuItems.map((item) => (
            <button
              key={item.key}
              type="button"
              className={activePage === item.key ? "menu-item active" : "menu-item"}
              onClick={() => setActivePage(item.key)}
            >
              <span className="menu-icon">{item.icon}</span>
              <span>
                <strong>{item.label}</strong>
                <small>{item.description}</small>
              </span>
            </button>
          ))}
        </nav>

        <div className="sider-note">
          <span>当前阶段</span>
          <strong>RAG MVP</strong>
          <small>不做 Agent，不做复杂权限，优先保证链路可靠。</small>
        </div>
      </aside>

      <div className="pro-main">
        <header className="pro-header">
          <div>
            <p className="breadcrumb">首页 / {current.title}</p>
            <h1>{current.title}</h1>
            <p>{current.subtitle}</p>
          </div>
          <div className="header-status">
            <span className="status-dot" />
            <span>本地开发环境</span>
          </div>
        </header>

        <main className="pro-content">
          {activePage === "knowledge" ? <KnowledgeBasePage /> : <RepairChatPage />}
        </main>
      </div>
    </div>
  );
}
