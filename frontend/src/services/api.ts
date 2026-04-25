import axios from "axios"

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

export interface CodeGenerationPayload {
  content: string
  session_id?: string | null
  model?: string
  api_key?: string | null
}

export interface CodeExplanationPayload {
  content: string
  code_snippet?: string | null
  session_id?: string | null
  model?: string
  api_key?: string | null
}

export interface CodeExecutionPayload {
  code: string
}

export async function generateCode(payload: CodeGenerationPayload) {
  const res = await api.post("/api/v1/chat/code", payload)
  return res.data
}

export async function explainCode(payload: CodeExplanationPayload) {
  const res = await api.post("/api/v1/chat/explain", payload)
  return res.data
}

export async function executeCode(payload: CodeExecutionPayload) {
  const res = await api.post("/api/v1/code/execute", payload)
  return res.data
}

export default api
