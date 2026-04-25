export interface ChatMessage {
  id: string
  role: "user" | "assistant" | "system"
  content: string
  timestamp: number
}

export interface CodeSnippet {
  code: string
  language: string
}

export interface SessionState {
  sessionId: string | null
  messages: ChatMessage[]
  isLoading: boolean
}

export interface ApiKeyState {
  apiKey: string | null
  isSet: boolean
}
