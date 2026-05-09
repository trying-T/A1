import { requestJson } from "./client";
import type { RepairChatRequest, RepairChatResponse } from "../types/repairChat";

export function repairChat(payload: RepairChatRequest) {
  return requestJson<RepairChatResponse>("/chat/repair", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
