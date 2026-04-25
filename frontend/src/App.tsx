import DualPanelLayout from '@/components/layout/DualPanelLayout'
import CodeChatPanel from '@/components/chat/CodeChatPanel'
import ExplainPanel from '@/components/chat/ExplainPanel'

function App() {
  return (
    <DualPanelLayout
      leftPanel={<CodeChatPanel />}
      rightPanel={<ExplainPanel />}
    />
  )
}

export default App
