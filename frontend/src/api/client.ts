const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api";

export async function requestJson<T>(input: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${input}`, init);
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const detail =
      payload && typeof payload === "object" && "detail" in payload
        ? String(payload.detail)
        : "请求失败，请稍后重试。";
    throw new Error(detail);
  }

  return payload as T;
}

export async function uploadFormData<T>(input: string, formData: FormData): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${input}`, {
    method: "POST",
    body: formData,
  });
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const detail =
      payload && typeof payload === "object" && "detail" in payload
        ? String(payload.detail)
        : "上传失败，请稍后重试。";
    throw new Error(detail);
  }

  return payload as T;
}
