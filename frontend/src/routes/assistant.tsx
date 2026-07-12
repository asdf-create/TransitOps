import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../lib/api'

export const Route = createFileRoute('/assistant')({
  component: Assistant,
})

function Assistant() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I\'m your AI assistant for TransitOps. I can help you analyze fleet data, provide insights, and answer questions about your operations. What would you like to know?' }
  ])
  const [input, setInput] = useState('')

  const chatMutation = useMutation({
    mutationFn: (message: string) => api.post('/ai/chat', {
      messages: [...messages, { role: 'user', content: message }],
      max_tokens: 512,
      temperature: 0.7
    }),
    onSuccess: (data) => {
      setMessages(prev => [...prev, { role: 'assistant', content: data.message }])
    }
  })

  const analyzeMutation = useMutation({
    mutationFn: (question: string) => api.post('/ai/analyze', {
      question,
      context: 'fleet-operations'
    }),
    onSuccess: (data) => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `${data.answer}\n\n**Insights:**\n${data.insights.map(i => `• ${i}`).join('\n')}\n\n**Recommendations:**\n${data.recommendations.map(r => `• ${r}`).join('\n')}`
      }])
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = input.trim()
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setInput('')

    // Use chat or analyze based on input
    if (userMessage.toLowerCase().includes('analyze') || userMessage.toLowerCase().includes('insight')) {
      analyzeMutation.mutate(userMessage)
    } else {
      chatMutation.mutate(userMessage)
    }
  }

  const quickQuestions = [
    "What is the current fleet status?",
    "Show me fuel efficiency analysis",
    "Analyze driver performance",
    "What are the maintenance needs?",
    "Generate fleet recommendations"
  ]

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">AI Assistant</h2>
      
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Chat with AI Assistant</h3>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <span className="text-sm text-gray-600">Online</span>
            </div>
          </div>
          
          <div className="border rounded-lg p-4 h-96 overflow-y-auto mb-4 bg-gray-50">
            {messages.map((msg, index) => (
              <div key={index} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                <div className={`inline-block max-w-[80%] p-3 rounded-lg ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-white border shadow-sm'
                }`}>
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
            {(chatMutation.isPending || analyzeMutation.isPending) && (
              <div className="text-left">
                <div className="inline-block bg-white border shadow-sm p-3 rounded-lg">
                  <p className="text-sm text-gray-500">Thinking...</p>
                </div>
              </div>
            )}
          </div>
          
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about fleet status, efficiency, maintenance..."
              className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={chatMutation.isPending || analyzeMutation.isPending}
            />
            <button
              type="submit"
              disabled={chatMutation.isPending || analyzeMutation.isPending || !input.trim()}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400"
            >
              Send
            </button>
          </form>
          
          <div className="mt-4">
            <p className="text-sm text-gray-600 mb-2">Quick questions:</p>
            <div className="flex flex-wrap gap-2">
              {quickQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => setInput(question)}
                  className="text-sm bg-gray-100 hover:bg-gray-200 px-3 py-1 rounded-full"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">AI Capabilities</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="border rounded-lg p-4">
              <h4 className="font-semibold mb-2">Fleet Analysis</h4>
              <p className="text-sm text-gray-600">Analyze vehicle performance, utilization, and operational efficiency</p>
            </div>
            <div className="border rounded-lg p-4">
              <h4 className="font-semibold mb-2">Predictive Insights</h4>
              <p className="text-sm text-gray-600">Get predictions for maintenance needs and potential issues</p>
            </div>
            <div className="border rounded-lg p-4">
              <h4 className="font-semibold mb-2">Route Optimization</h4>
              <p className="text-sm text-gray-600">Receive recommendations for efficient route planning</p>
            </div>
            <div className="border rounded-lg p-4">
              <h4 className="font-semibold mb-2">Driver Performance</h4>
              <p className="text-sm text-gray-600">Analyze driver safety scores and productivity metrics</p>
            </div>
            <div className="border rounded-lg p-4">
              <h4 className="font-semibold mb-2">Cost Analysis</h4>
              <p className="text-sm text-gray-600">Break down operational costs and identify savings opportunities</p>
            </div>
            <div className="border rounded-lg p-4">
              <h4 className="font-semibold mb-2">Offline Processing</h4>
              <p className="text-sm text-gray-600">All AI processing runs locally using llama.cpp</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}