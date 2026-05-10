import { useState } from "react";

import BasicLayout from "./layouts/BasicLayout";
import KnowledgeBasePage from "./pages/KnowledgeBasePage";
import RepairChatPage from "./pages/RepairChatPage";
import WorkOrderPage from "./pages/WorkOrderPage";

type ActivePage = "knowledge" | "repair" | "workorders";

export default function App() {
  const [activePage, setActivePage] = useState<ActivePage>("knowledge");
  const [selectedWorkOrderId, setSelectedWorkOrderId] = useState<string | null>(null);

  function handleWorkOrderCreated(workOrderId: string) {
    setSelectedWorkOrderId(workOrderId);
    setActivePage("workorders");
  }

  return (
    <BasicLayout activePage={activePage} onPageChange={setActivePage}>
      {activePage === "knowledge" ? <KnowledgeBasePage /> : null}
      {activePage === "repair" ? <RepairChatPage onWorkOrderCreated={handleWorkOrderCreated} /> : null}
      {activePage === "workorders" ? <WorkOrderPage selectedWorkOrderId={selectedWorkOrderId} /> : null}
    </BasicLayout>
  );
}
