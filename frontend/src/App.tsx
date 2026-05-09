import { useState } from "react";

import KnowledgeBasePage from "./pages/KnowledgeBasePage";
import RepairChatPage from "./pages/RepairChatPage";

type ActivePage = "knowledge" | "repair";

export default function App() {
  const [activePage, setActivePage] = useState<ActivePage>("knowledge");

  return (
    <>
      <nav className="top-nav">
        <button
          className={activePage === "knowledge" ? "nav-tab active" : "nav-tab"}
          type="button"
          onClick={() => setActivePage("knowledge")}
        >
          知识库
        </button>
        <button
          className={activePage === "repair" ? "nav-tab active" : "nav-tab"}
          type="button"
          onClick={() => setActivePage("repair")}
        >
          检修问答
        </button>
      </nav>
      {activePage === "knowledge" ? <KnowledgeBasePage /> : <RepairChatPage />}
    </>
  );
}
