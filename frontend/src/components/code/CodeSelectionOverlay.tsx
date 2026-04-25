import { CircleHelp } from "lucide-react"

interface CodeSelectionOverlayProps {
  visible: boolean
  position: { top: number; left: number }
  onAsk: () => void
  onMouseEnter: () => void
  onMouseLeave: () => void
}

export default function CodeSelectionOverlay({
  visible,
  position,
  onAsk,
  onMouseEnter,
  onMouseLeave,
}: CodeSelectionOverlayProps) {
  if (!visible) return null

  return (
    <button
      type="button"
      onClick={onAsk}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
      style={{
        position: "fixed",
        top: position.top,
        left: position.left,
        zIndex: 50,
      }}
      className="flex items-center gap-1 rounded-full bg-primary px-3 py-1.5 text-xs font-medium text-primary-foreground shadow-lg transition-colors hover:bg-primary/90"
      aria-label="Ask about selected code"
    >
      <CircleHelp className="h-3 w-3" />
      Ask
    </button>
  )
}
