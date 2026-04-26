import { useState, useEffect, useRef, useCallback } from "react"
import { useChatStore } from "@/stores/chatStore"
import { useUIStore } from "@/stores/uiStore"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { chatWS } from "@/services/websocket"

export default function ExplainPanel() {
  const [input, setInput] = useState("")
  const {
    explainMessages,
    explainSessionId,
    isExplainLoading,
    addExplainMessage,
    setExplainSessionId,
    setExplainLoading,
  } = useChatStore()
  const { selectedSnippet, setSelectedSnippet, apiKey } = useUIStore()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const currentResponseRef = useRef("")

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [explainMessages])

  useEffect(() => {
    if (!explainSessionId) {
      setExplainSessionId(crypto.randomUUID())
    }
  }, [explainSessionId, setExplainSessionId])

  useEffect(() => {
    if (!selectedSnippet) return

    setInput(
      `我对这段代码有疑问：\n\n\`\`\`${selectedSnippet.language}\n${selectedSnippet.code}\n\`\`\`\n\n`
    )
    window.setTimeout(() => {
      inputRef.current?.focus()
      inputRef.current?.setSelectionRange(
        inputRef.current.value.length,
        inputRef.current.value.length
      )
    }, 0)
  }, [selectedSnippet])

  useEffect(() => {
    const unsub = chatWS.onMessage((msg) => {
      if (msg.type === "chat.chunk") {
        if (msg.payload.session_id !== useChatStore.getState().explainSessionId) return
        const chunk = msg.payload.content as string
        currentResponseRef.current += chunk
        const messages = useChatStore.getState().explainMessages
        const lastMsg = messages[messages.length - 1]
        if (lastMsg && lastMsg.role === "assistant") {
          useChatStore.setState({
            explainMessages: messages.slice(0, -1).concat({
              ...lastMsg,
              content: currentResponseRef.current,
            }),
          })
        }
      }
      if (msg.type === "chat.done") {
        if (msg.payload.session_id !== useChatStore.getState().explainSessionId) return
        setExplainLoading(false)
        currentResponseRef.current = ""
      }
      if (msg.type === "error") {
        setExplainLoading(false)
        addExplainMessage({
          role: "assistant",
          content: `Error: ${msg.payload.message}`,
        })
        currentResponseRef.current = ""
      }
    })

    return () => {
      unsub()
    }
  }, [setExplainLoading, addExplainMessage])

  const handleSend = useCallback(() => {
    if (!input.trim() || isExplainLoading) return

    const sessionId = explainSessionId ?? crypto.randomUUID()
    if (!explainSessionId) {
      setExplainSessionId(sessionId)
    }

    addExplainMessage({ role: "user", content: input.trim() })
    addExplainMessage({ role: "assistant", content: "" })
    setExplainLoading(true)
    currentResponseRef.current = ""

    chatWS.send({
      type: "chat.message",
      payload: {
        content: input.trim(),
        mode: "explain",
        session_id: sessionId,
        code_snippet: selectedSnippet?.code,
        ...(apiKey ? { api_key: apiKey } : {}),
      },
    })

    setInput("")
  }, [
    input,
    isExplainLoading,
    apiKey,
    addExplainMessage,
    setExplainLoading,
    explainSessionId,
    setExplainSessionId,
    selectedSnippet,
  ])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="h-12 border-b flex items-center px-4 shrink-0 justify-between">
        <h2 className="text-sm font-medium">理解助手</h2>
        {selectedSnippet && (
          <span className="text-xs text-muted-foreground">已选中代码片段</span>
        )}
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {selectedSnippet && (
          <div className="bg-muted rounded-lg p-3 text-xs relative group">
            <div className="font-medium mb-1 text-muted-foreground">代码片段上下文</div>
            <pre className="font-mono text-[11px] overflow-x-auto whitespace-pre-wrap break-all">
              {selectedSnippet.code}
            </pre>
            <button
              onClick={() => setSelectedSnippet(null)}
              className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-foreground"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        )}

        {explainMessages.length === 0 && (
          <div className="text-center text-muted-foreground text-sm py-8">
            {selectedSnippet
              ? "在下方输入你对这段代码的疑问"
              : "在编程通道选中代码点击 Ask，或直接在此提问"}
          </div>
        )}

        {explainMessages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[90%] rounded-lg px-4 py-2 text-sm ${
                msg.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted"
              }`}
            >
              <div className="whitespace-pre-wrap">{msg.content || "..."}</div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4 shrink-0">
        <div className="flex gap-2">
          <Textarea
            id="explain-panel-input"
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={selectedSnippet ? "询问关于选中代码的问题..." : "提问或让 AI 解释代码..."}
            className="min-h-[60px] resize-none"
            disabled={isExplainLoading}
          />
          <Button
            onClick={handleSend}
            disabled={isExplainLoading || !input.trim()}
            className="shrink-0 self-end h-[60px] px-4"
          >
            {isExplainLoading ? (
              <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"/>
                <polygon points="22 2 15 22 11 13 2 9 22 2"/>
              </svg>
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}
