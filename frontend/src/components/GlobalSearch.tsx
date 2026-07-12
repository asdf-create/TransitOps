import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Truck, Users, Route, X } from 'lucide-react'
import { useNavigate } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

interface SearchResult {
  id: string | number
  label: string
  sub: string
  type: 'vehicle' | 'driver' | 'trip'
  to: string
}

interface Props {
  open: boolean
  onClose: () => void
}

const typeIcon = {
  vehicle: <Truck className="w-4 h-4 text-blue-400" />,
  driver: <Users className="w-4 h-4 text-green-400" />,
  trip: <Route className="w-4 h-4 text-purple-400" />,
}

const typeLabel = {
  vehicle: 'Vehicles',
  driver: 'Drivers',
  trip: 'Trips',
}

export function GlobalSearch({ open, onClose }: Props) {
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState(0)
  const inputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  const { data: vehicles } = useQuery({ queryKey: ['vehicles'], queryFn: () => api.get('/vehicles'), enabled: open })
  const { data: drivers } = useQuery({ queryKey: ['drivers'], queryFn: () => api.get('/drivers'), enabled: open })
  const { data: trips } = useQuery({ queryKey: ['trips'], queryFn: () => api.get('/trips'), enabled: open })

  const results: SearchResult[] = []

  if (vehicles && query) {
    vehicles
      .filter((v: any) =>
        v.registration_number?.toLowerCase().includes(query.toLowerCase()) ||
        v.model?.toLowerCase().includes(query.toLowerCase())
      )
      .slice(0, 3)
      .forEach((v: any) =>
        results.push({ id: v.id, label: v.registration_number, sub: `${v.model} • ${v.status}`, type: 'vehicle', to: '/vehicles' })
      )
  }

  if (drivers && query) {
    drivers
      .filter((d: any) => d.full_name?.toLowerCase().includes(query.toLowerCase()))
      .slice(0, 3)
      .forEach((d: any) =>
        results.push({ id: d.id, label: d.full_name, sub: `License: ${d.license_number} • ${d.status}`, type: 'driver', to: '/drivers' })
      )
  }

  if (trips && query) {
    trips
      .filter((t: any) =>
        t.tracking_id?.toLowerCase().includes(query.toLowerCase()) ||
        t.source?.toLowerCase().includes(query.toLowerCase()) ||
        t.destination?.toLowerCase().includes(query.toLowerCase())
      )
      .slice(0, 3)
      .forEach((t: any) =>
        results.push({ id: t.id, label: t.tracking_id, sub: `${t.source} → ${t.destination} • ${t.status}`, type: 'trip', to: '/trips' })
      )
  }

  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 50)
      setQuery('')
      setSelected(0)
    }
  }, [open])

  useEffect(() => { setSelected(0) }, [query])

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (!open) return
      if (e.key === 'ArrowDown') { e.preventDefault(); setSelected(s => Math.min(s + 1, results.length - 1)) }
      if (e.key === 'ArrowUp') { e.preventDefault(); setSelected(s => Math.max(s - 1, 0)) }
      if (e.key === 'Enter' && results[selected]) {
        navigate({ to: results[selected].to })
        onClose()
      }
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [open, results, selected, navigate, onClose])

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.97, y: -8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.97, y: -8 }}
            transition={{ duration: 0.15, ease: [0.4, 0, 0.2, 1] }}
            className="fixed top-[15%] left-1/2 -translate-x-1/2 z-50 w-full max-w-xl"
          >
            <div className="rounded-xl border border-white/[0.10] bg-gray-900 shadow-2xl overflow-hidden">
              {/* Input */}
              <div className="flex items-center px-4 gap-3 border-b border-white/[0.06]">
                <Search className="w-4 h-4 text-gray-500 flex-shrink-0" />
                <input
                  ref={inputRef}
                  value={query}
                  onChange={e => setQuery(e.target.value)}
                  placeholder="Search vehicles, drivers, trips..."
                  className="flex-1 h-12 bg-transparent text-sm text-gray-100 placeholder:text-gray-500 outline-none"
                />
                <button onClick={onClose} className="text-gray-600 hover:text-gray-400 transition-colors">
                  <X className="w-4 h-4" />
                </button>
              </div>

              {/* Results */}
              <div className="max-h-80 overflow-y-auto">
                {!query && (
                  <div className="px-4 py-8 text-center text-sm text-gray-500">
                    Start typing to search across vehicles, drivers, and trips
                  </div>
                )}
                {query && results.length === 0 && (
                  <div className="px-4 py-8 text-center text-sm text-gray-500">
                    No results for "{query}"
                  </div>
                )}
                {results.length > 0 && (
                  <div className="py-2">
                    {(['vehicle', 'driver', 'trip'] as const).map(type => {
                      const group = results.filter(r => r.type === type)
                      if (group.length === 0) return null
                      return (
                        <div key={type}>
                          <div className="px-4 py-1.5 text-[10px] font-semibold text-gray-600 uppercase tracking-wider">
                            {typeLabel[type]}
                          </div>
                          {group.map(result => {
                            const idx = results.indexOf(result)
                            return (
                              <button
                                key={result.id}
                                onClick={() => { navigate({ to: result.to }); onClose() }}
                                className={`w-full flex items-center gap-3 px-4 py-2.5 text-left transition-colors ${
                                  selected === idx ? 'bg-white/[0.06]' : 'hover:bg-white/[0.03]'
                                }`}
                              >
                                <div className="flex-shrink-0">{typeIcon[result.type]}</div>
                                <div className="min-w-0">
                                  <p className="text-sm text-gray-100 truncate">{result.label}</p>
                                  <p className="text-xs text-gray-500 truncate">{result.sub}</p>
                                </div>
                              </button>
                            )
                          })}
                        </div>
                      )
                    })}
                  </div>
                )}
              </div>

              {/* Footer hint */}
              <div className="flex items-center gap-4 px-4 py-2 border-t border-white/[0.06] text-[10px] text-gray-600">
                <span>↑↓ navigate</span>
                <span>↵ select</span>
                <span>Esc close</span>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
