import { useRef, useCallback, useState, useEffect } from "react"
import Editor from "@monaco-editor/react"
import type { editor as MonacoEditor } from "monaco-editor"
import { useUIStore } from "@/stores/uiStore"
import CodeSelectionOverlay from "@/components/code/CodeSelectionOverlay"

interface CodeEditorProps {
  code: string
  language?: string
  readOnly?: boolean
  height?: string
}

export default function CodeEditor({
  code,
  language = "python",
  readOnly = true,
  height = "300px",
}: CodeEditorProps) {
  const editorRef = useRef<MonacoEditor.IStandaloneCodeEditor | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)
  const { setSelectedSnippet } = useUIStore()
  const [showAsk, setShowAsk] = useState(false)
  const [askPos, setAskPos] = useState({ top: 0, left: 0 })
  const pendingSnippet = useRef<{ code: string; language: string } | null>(null)
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const clearHideTimer = () => {
    if (hideTimer.current) {
      clearTimeout(hideTimer.current)
      hideTimer.current = null
    }
  }

  const scheduleHide = () => {
    clearHideTimer()
    hideTimer.current = setTimeout(() => {
      setShowAsk(false)
    }, 3000)
  }

  const handleAskClick = () => {
    if (pendingSnippet.current) {
      setSelectedSnippet(pendingSnippet.current)
      setShowAsk(false)
      clearHideTimer()
      // Scroll explain panel into view on mobile if needed
      const explainPanel = document.getElementById("explain-panel-input")
      explainPanel?.focus()
    }
  }

  const handleEditorDidMount = useCallback(
    (editor: MonacoEditor.IStandaloneCodeEditor) => {
      editorRef.current = editor

      editor.onMouseUp(() => {
        const selection = editor.getSelection()
        if (!selection || selection.isEmpty()) {
          setShowAsk(false)
          clearHideTimer()
          return
        }

        const model = editor.getModel()
        if (!model) return

        const selectedText = model.getValueInRange(selection)
        if (selectedText.trim().length === 0) {
          setShowAsk(false)
          clearHideTimer()
          return
        }

        pendingSnippet.current = { code: selectedText, language }

        const pos = editor.getScrolledVisiblePosition(selection.getEndPosition())
        if (pos && containerRef.current) {
          const containerRect = containerRef.current.getBoundingClientRect()
          setAskPos({
            top: pos.top + containerRect.top + 20,
            left: pos.left + containerRect.left + 10,
          })
        }

        setShowAsk(true)
        scheduleHide()
      })

      editor.onDidBlurEditorText(() => {
        setShowAsk(false)
        clearHideTimer()
      })
    },
    [language]
  )

  useEffect(() => {
    return () => clearHideTimer()
  }, [])

  return (
    <div ref={containerRef} className="relative border rounded-md overflow-hidden">
      <Editor
        height={height}
        language={language}
        value={code}
        theme="vs-dark"
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 14,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          wordWrap: "on",
        }}
        onMount={handleEditorDidMount}
      />

      <CodeSelectionOverlay
        visible={showAsk}
        position={askPos}
        onAsk={handleAskClick}
        onMouseEnter={clearHideTimer}
        onMouseLeave={scheduleHide}
      />
    </div>
  )
}
