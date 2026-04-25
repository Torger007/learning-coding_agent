import { create } from "zustand"
import type { ChatMessage } from "@/types"

interface ChatState {
  codeMessages: ChatMessage[]
  explainMessages: ChatMessage[]
  codeSessionId: string | null
  explainSessionId: string | null
  isCodeLoading: boolean
  isExplainLoading: boolean
  addCodeMessage: (message: Omit<ChatMessage, "id" | "timestamp">) => void
  addExplainMessage: (message: Omit<ChatMessage, "id" | "timestamp">) => void
  setCodeSessionId: (id: string | null) => void
  setExplainSessionId: (id: string | null) => void
  setCodeLoading: (loading: boolean) => void
  setExplainLoading: (loading: boolean) => void
  clearCodeMessages: () => void
  clearExplainMessages: () => void
}

const generateId = () => Math.random().toString(36).substring(2, 9)

export const useChatStore = create<ChatState>((set) => ({
  codeMessages: [],
  explainMessages: [],
  codeSessionId: null,
  explainSessionId: null,
  isCodeLoading: false,
  isExplainLoading: false,

  addCodeMessage: (message) =>
    set((state) => ({
      codeMessages: [
        ...state.codeMessages,
        { ...message, id: generateId(), timestamp: Date.now() },
      ],
    })),

  addExplainMessage: (message) =>
    set((state) => ({
      explainMessages: [
        ...state.explainMessages,
        { ...message, id: generateId(), timestamp: Date.now() },
      ],
    })),

  setCodeSessionId: (id) => set({ codeSessionId: id }),
  setExplainSessionId: (id) => set({ explainSessionId: id }),
  setCodeLoading: (loading) => set({ isCodeLoading: loading }),
  setExplainLoading: (loading) => set({ isExplainLoading: loading }),
  clearCodeMessages: () => set({ codeMessages: [], codeSessionId: null }),
  clearExplainMessages: () => set({ explainMessages: [], explainSessionId: null }),
}))
