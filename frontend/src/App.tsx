import { useState } from "react";

import BasicLayout from "./layouts/BasicLayout";
import KnowledgeBasePage from "./pages/KnowledgeBasePage";
import RepairChatPage from "./pages/RepairChatPage";
import WorkOrderPage from "./pages/WorkOrderPage";

type ActivePage = "knowledge" | "repair" | "workorders";

export default function App() {
  const [activePage, setActivePage] = useState<ActivePage>("knowledge");

  return (
    <BasicLayout activePage={activePage} onPageChange={setActivePage}>
      {activePage === "knowledge" ? <KnowledgeBasePage /> : null}
      {activePage === "repair" ? <RepairChatPage /> : null}
      {activePage === "workorders" ? <WorkOrderPage /> : null}
    </BasicLayout>
  );
}
