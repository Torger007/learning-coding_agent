import { useState } from "react"
import { useUIStore } from "@/stores/uiStore"
import {
  Dialog,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

interface ApiKeySettingsProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export default function ApiKeySettings({ open, onOpenChange }: ApiKeySettingsProps) {
  const { apiKey, setApiKey } = useUIStore()
  const [key, setKey] = useState(apiKey || "")
  const [showKey, setShowKey] = useState(false)
  const [showGuide, setShowGuide] = useState(false)

  const handleSave = () => {
    if (key.trim()) {
      setApiKey(key.trim())
      onOpenChange(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogHeader>
        <DialogTitle>设置 API Key</DialogTitle>
        <DialogDescription>
          请输入你的 Kimi API Key 以使用 AI 功能
        </DialogDescription>
      </DialogHeader>

      <div className="space-y-4 py-4">
        <div className="space-y-2">
          <label className="text-sm font-medium">API Key</label>
          <div className="flex gap-2">
            <input
              type={showKey ? "text" : "password"}
              value={key}
              onChange={(e) => setKey(e.target.value)}
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
              className="flex-1 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            />
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setShowKey(!showKey)}
            >
              {showKey ? "隐藏" : "显示"}
            </Button>
          </div>
        </div>

        <div className="border rounded-md">
          <button
            onClick={() => setShowGuide(!showGuide)}
            className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium hover:bg-muted transition-colors"
          >
            <span>如何获取 API Key？</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className={`transition-transform ${showGuide ? "rotate-180" : ""}`}
            >
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>

          {showGuide && (
            <div className="px-4 pb-4 text-sm text-muted-foreground space-y-3">
              <ol className="list-decimal list-inside space-y-2">
                <li>
                  访问 Kimi 开放平台：
                  <a
                    href="https://platform.moonshot.cn"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary underline"
                  >
                    platform.moonshot.cn
                  </a>
                </li>
                <li>注册或登录你的账号</li>
                <li>进入左侧菜单「API Key 管理」页面</li>
                <li>点击「创建 API Key」按钮</li>
                <li>复制生成的 Key（以 sk- 开头），粘贴到上方输入框</li>
                <li>点击「保存」按钮完成设置</li>
              </ol>
              <p className="text-xs text-muted-foreground bg-muted p-2 rounded">
                注意：API Key 仅保存在当前页面内存中，刷新页面后需要重新输入。
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="flex justify-end gap-2">
        <Button variant="outline" onClick={() => onOpenChange(false)}>
          取消
        </Button>
        <Button onClick={handleSave} disabled={!key.trim()}>
          保存
        </Button>
      </div>
    </Dialog>
  )
}
