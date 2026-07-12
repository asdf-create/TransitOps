import { createFileRoute } from '@tanstack/react-router'
import { useState, useRef, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../lib/api'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import { Send, Bot, User, Trash2, HelpCircle, AlertCircle } from 'lucide-react'
import { Card, CardContent } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'

export const Route = createFileRoute('/assistant')({
  component: Assistant,
})

interface Message {
  role: 'assistant' | 'user'
  content: string
}

const QUICK_ACTIONS = [
  { label: 'Fleet Status', query: 'Show vehicle status and utilization summary' },
  { label: 'Driver Status', query: 'Show active and available driver statistics' },
  { label: 'Fuel & Costs', query: 'Show fuel logs and operating costs details' },
  { label: 'Maintenance Alerts', query: 'Which vehicles are currently in maintenance?' },
]

function Assistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content:
        "Hello! I'm your TransitOps AI Assistant. Operating entirely offline on local llama.cpp, I can help you analyze fleet operations, driver safety rankings, maintenance history, and trip statuses. Try a quick action below or ask any question!",
    },
  ])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const chatMutation = useMutation({
    mutationFn: (userQuery: string) =>
      api.post('/ai/chat', {
        messages: [...messages, { role: 'user', content: userQuery }],
        max_tokens: 512,
        temperature: 0.7,
      }),
    onSuccess: (data) => {
      setMessages((prev) => [...prev, { role: 'assistant', content: data.message }])
    },
    onError: () => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '⚠️ Failed to connect to the local AI backend. Please verify that the TransitOps server is running.',
        },
      ])
    },
  })

  const handleSendMessage = (textToSend: string) => {
    if (!textToSend.trim() || chatMutation.isPending) return

    setMessages((prev) => [...prev, { role: 'user', content: textToSend }])
    setInput('')
    chatMutation.mutate(textToSend)
  }

  const handleClearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: 'Conversation history cleared. How can I help you manage your fleet operations today?',
      },
    ])
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-4xl mx-auto bg-white/[0.01] border border-white/[0.06] rounded-xl overflow-hidden backdrop-blur-md">
      {/* Assistant Header */}
      <div className="flex justify-between items-center px-6 py-4 border-b border-white/[0.06] bg-gray-950/40">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <Bot className="w-4.5 h-4.5" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-gray-200">Local AI Assistant</h2>
            <p className="text-[10px] text-gray-400">llama.cpp • 100% Offline</p>
          </div>
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={handleClearChat}
          className="text-gray-400 hover:text-red-400 hover:bg-red-500/10"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-thin">
        <AnimatePresence initial={false}>
          {messages.map((msg, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className={`flex gap-3 max-w-[85%] ${
                msg.role === 'user' ? 'ml-auto flex-row-reverse' : ''
              }`}
            >
              <div
                className={`w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center border text-xs ${
                  msg.role === 'user'
                    ? 'bg-blue-600/20 border-blue-500/30 text-blue-400'
                    : 'bg-white/5 border-white/10 text-gray-300'
                }`}
              >
                {msg.role === 'user' ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
              </div>

              <div
                className={`rounded-xl px-4 py-2.5 text-xs line-height-relaxed border ${
                  msg.role === 'user'
                    ? 'bg-blue-600/15 border-blue-500/20 text-blue-100'
                    : 'bg-white/[0.02] border-white/[0.05] text-gray-200'
                }`}
              >
                <ReactMarkdown className="prose prose-invert prose-xs max-w-none">
                  {msg.content}
                </ReactMarkdown>
              </div>
            </motion.div>
          ))}

          {chatMutation.isPending && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex gap-3 max-w-[85%]"
            >
              <div className="w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center border bg-white/5 border-white/10 text-gray-300">
                <Bot className="w-3.5 h-3.5 animate-pulse" />
              </div>
              <div className="bg-white/[0.02] border border-white/[0.05] rounded-xl px-4 py-3.5 flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '150ms' }} />
                <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input panel & suggestions */}
      <div className="p-4 border-t border-white/[0.06] bg-gray-950/20 space-y-4">
        {/* Quick Action Suggestions */}
        {messages.length === 1 && (
          <div className="flex flex-wrap gap-2 justify-center">
            {QUICK_ACTIONS.map((action, idx) => (
              <button
                key={idx}
                onClick={() => handleSendMessage(action.query)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-white/[0.06] bg-white/[0.02] hover:bg-white/[0.06] hover:border-white/[0.1] text-[10px] text-gray-300 transition-all"
              >
                <HelpCircle className="w-3 h-3 text-blue-400" />
                <span>{action.label}</span>
              </button>
            ))}
          </div>
        )}

        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleSendMessage(input)
          }}
          className="flex gap-2"
        >
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about active trips, drivers, fuel efficiency..."
            disabled={chatMutation.isPending}
            className="flex-1 bg-white/[0.02] border-white/[0.08] focus-visible:ring-blue-500/50 text-xs h-9"
          />
          <Button
            type="submit"
            disabled={chatMutation.isPending || !input.trim()}
            className="bg-blue-600 hover:bg-blue-500 text-white px-3.5 h-9"
          >
            <Send className="w-4 h-4" />
          </Button>
        </form>
      </div>
    </div>
  )
}