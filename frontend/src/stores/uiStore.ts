import { create } from "zustand"
import type { CodeSnippet } from "@/types"

interface UIState {
  selectedSnippet: CodeSnippet | null
  apiKey: string | null
  showApiKeyDialog: boolean
  setSelectedSnippet: (snippet: CodeSnippet | null) => void
  setApiKey: (key: string | null) => void
  setShowApiKeyDialog: (show: boolean) => void
}

export const useUIStore = create<UIState>((set) => ({
  selectedSnippet: null,
  apiKey: null,
  showApiKeyDialog: false,
  setSelectedSnippet: (snippet) => set({ selectedSnippet: snippet }),
  setApiKey: (key) => set({ apiKey: key }),
  setShowApiKeyDialog: (show) => set({ showApiKeyDialog: show }),
}))
