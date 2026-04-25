import { useState, useEffect, useRef, useCallback } from "react"
import { useChatStore } from "@/stores/chatStore"
import { useUIStore } from "@/stores/uiStore"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { chatWS } from "@/services/websocket"
import CodeEditor from "@/components/code/CodeEditor"

export default function CodeChatPanel() {
  const [input, setInput] = useState("")
  const {
    codeMessages,
    codeSessionId,
    isCodeLoading,
    addCodeMessage,
    setCodeSessionId,
    setCodeLoading,
  } = useChatStore()
  const { apiKey } = useUIStore()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const currentResponseRef = useRef("")

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [codeMessages])

  useEffect(() => {
    if (!codeSessionId) {
      setCodeSessionId(crypto.randomUUID())
    }
  }, [codeSessionId, setCodeSessionId])

  useEffect(() => {
    chatWS.connect()

    const unsub = chatWS.onMessage((msg) => {
      if (msg.type === "chat.chunk") {
        if (msg.payload.session_id !== useChatStore.getState().codeSessionId) return
        const chunk = msg.payload.content as string
        currentResponseRef.current += chunk
        const messages = useChatStore.getState().codeMessages
        const lastMsg = messages[messages.length - 1]
        if (lastMsg && lastMsg.role === "assistant") {
          useChatStore.setState({
            codeMessages: messages.slice(0, -1).concat({
              ...lastMsg,
              content: currentResponseRef.current,
            }),
          })
        }
      }
      if (msg.type === "chat.done") {
        if (msg.payload.session_id !== useChatStore.getState().codeSessionId) return
        setCodeLoading(false)
        currentResponseRef.current = ""
      }
      if (msg.type === "error") {
        setCodeLoading(false)
        addCodeMessage({
          role: "assistant",
          content: `Error: ${msg.payload.message}`,
        })
        currentResponseRef.current = ""
      }
    })

    return () => {
      unsub()
    }
  }, [setCodeLoading, addCodeMessage])

  const handleSend = useCallback(() => {
    if (!input.trim() || isCodeLoading) return
    if (!apiKey) {
      useUIStore.getState().setShowApiKeyDialog(true)
      return
    }

    const sessionId = codeSessionId ?? crypto.randomUUID()
    if (!codeSessionId) {
      setCodeSessionId(sessionId)
    }

    addCodeMessage({ role: "user", content: input.trim() })
    addCodeMessage({ role: "assistant", content: "" })
    setCodeLoading(true)
    currentResponseRef.current = ""

    chatWS.send({
      type: "chat.message",
      payload: {
        content: input.trim(),
        mode: "code",
        session_id: sessionId,
        api_key: apiKey,
      },
    })

    setInput("")
  }, [input, isCodeLoading, apiKey, addCodeMessage, setCodeLoading, codeSessionId, setCodeSessionId])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const extractCodeBlock = (content: string) => {
    const match = content.match(/```(\w+)?\n([\s\S]*?)```/)
    if (match) {
      return { language: match[1] || "python", code: match[2].trim() }
    }
    return null
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="h-12 border-b flex items-center px-4 shrink-0">
        <h2 className="text-sm font-medium">编程助手</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {codeMessages.length === 0 && (
          <div className="text-center text-muted-foreground text-sm py-8">
            在下方输入框描述你的编程需求，AI 将为你生成代码
          </div>
        )}
        {codeMessages.map((msg) => {
          const codeBlock = msg.role === "assistant" ? extractCodeBlock(msg.content) : null
          return (
            <div
              key={msg.id}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[85%] rounded-lg px-4 py-2 text-sm ${
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted"
                }`}
              >
                {codeBlock ? (
                  <div className="space-y-2">
                    <CodeEditor
                      code={codeBlock.code}
                      language={codeBlock.language}
                      readOnly
                      height="200px"
                    />
                    {msg.content.replace(/```[\s\S]*?```/, "").trim() && (
                      <p className="text-sm mt-2">{msg.content.replace(/```[\s\S]*?```/, "").trim()}</p>
                    )}
                  </div>
                ) : (
                  <div className="whitespace-pre-wrap">{msg.content || "..."}</div>
                )}
              </div>
            </div>
          )
        })}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4 shrink-0">
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="描述你的编程需求...（Shift+Enter 换行）"
            className="min-h-[60px] resize-none"
            disabled={isCodeLoading}
          />
          <Button
            onClick={handleSend}
            disabled={isCodeLoading || !input.trim()}
            className="shrink-0 self-end h-[60px] px-4"
          >
            {isCodeLoading ? (
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
