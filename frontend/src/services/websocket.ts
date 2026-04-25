const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || "ws://localhost:8000"

export type WSMessageType =
  | "chat.init"
  | "chat.init_ack"
  | "chat.message"
  | "chat.chunk"
  | "chat.done"
  | "error"

export interface WSMessage {
  type: WSMessageType
  payload: Record<string, unknown>
}

export class ChatWebSocket {
  private ws: WebSocket | null = null
  private messageCallbacks: ((msg: WSMessage) => void)[] = []
  private openCallbacks: (() => void)[] = []
  private closeCallbacks: (() => void)[] = []
  private pendingMessages: WSMessage[] = []

  connect() {
    if (this.ws) return
    this.ws = new WebSocket(`${WS_BASE_URL}/api/v1/ws/chat`)

    this.ws.onopen = () => {
      this.flushPendingMessages()
      this.openCallbacks.forEach((cb) => cb())
    }

    this.ws.onmessage = (event) => {
      try {
        const msg: WSMessage = JSON.parse(event.data)
        this.messageCallbacks.forEach((cb) => cb(msg))
      } catch {
        // ignore malformed messages
      }
    }

    this.ws.onclose = () => {
      this.closeCallbacks.forEach((cb) => cb())
      this.ws = null
    }

    this.ws.onerror = () => {
      this.ws?.close()
    }
  }

  disconnect() {
    this.ws?.close()
    this.ws = null
  }

  send(msg: WSMessage) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(msg))
      return
    }

    this.pendingMessages.push(msg)
    this.connect()
  }

  private flushPendingMessages() {
    if (this.ws?.readyState !== WebSocket.OPEN) return

    for (const msg of this.pendingMessages) {
      this.ws.send(JSON.stringify(msg))
    }
    this.pendingMessages = []
  }

  onMessage(cb: (msg: WSMessage) => void) {
    this.messageCallbacks.push(cb)
    return () => {
      this.messageCallbacks = this.messageCallbacks.filter((c) => c !== cb)
    }
  }

  onOpen(cb: () => void) {
    this.openCallbacks.push(cb)
    return () => {
      this.openCallbacks = this.openCallbacks.filter((c) => c !== cb)
    }
  }

  onClose(cb: () => void) {
    this.closeCallbacks.push(cb)
    return () => {
      this.closeCallbacks = this.closeCallbacks.filter((c) => c !== cb)
    }
  }
}

export const chatWS = new ChatWebSocket()
