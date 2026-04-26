import type { ReactNode } from "react"
import { useUIStore } from "@/stores/uiStore"
import { Button } from "@/components/ui/button"
import ApiKeySettings from "@/components/settings/ApiKeySettings"

interface DualPanelLayoutProps {
  leftPanel: ReactNode
  rightPanel: ReactNode
}

export default function DualPanelLayout({ leftPanel, rightPanel }: DualPanelLayoutProps) {
  const { apiKey, showApiKeyDialog, setShowApiKeyDialog } = useUIStore()

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="h-14 border-b flex items-center justify-between px-4 shrink-0">
        <div className="flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-primary">
            <polyline points="16 18 22 12 16 6"/>
            <polyline points="8 6 2 12 8 18"/>
          </svg>
          <h1 className="text-lg font-semibold">Coding Agent</h1>
        </div>
        <div className="flex items-center gap-2">
          {apiKey ? (
            <span className="text-xs text-muted-foreground">已使用前端 API Key</span>
          ) : (
            <Button size="sm" variant="outline" onClick={() => setShowApiKeyDialog(true)}>
              设置前端 API Key（可选）
            </Button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 border-r flex flex-col min-w-0">{leftPanel}</div>
        <div className="flex-1 flex flex-col min-w-0">{rightPanel}</div>
      </div>

      <ApiKeySettings open={showApiKeyDialog} onOpenChange={setShowApiKeyDialog} />
    </div>
  )
}
