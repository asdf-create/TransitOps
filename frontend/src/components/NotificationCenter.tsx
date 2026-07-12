import { motion, AnimatePresence } from 'framer-motion'
import { X, Bell, CheckCheck, AlertTriangle, Info, AlertCircle } from 'lucide-react'
import { useState } from 'react'
import { Badge } from './ui/badge'
import { Button } from './ui/button'

interface Notification {
  id: string
  title: string
  message: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  time: string
  read: boolean
}

const MOCK_NOTIFICATIONS: Notification[] = [
  {
    id: '1',
    title: 'Vehicle Maintenance Due',
    message: 'Vehicle KA-01-AB-1234 is due for scheduled maintenance in 2 days.',
    priority: 'high',
    time: '5 min ago',
    read: false,
  },
  {
    id: '2',
    title: 'Trip Completed',
    message: 'Trip TRK-1001 from Warehouse A to Warehouse B completed successfully.',
    priority: 'low',
    time: '23 min ago',
    read: false,
  },
  {
    id: '3',
    title: 'Driver Safety Alert',
    message: 'Driver Rahul Singh has a safety score drop. Review recommended.',
    priority: 'medium',
    time: '1 hr ago',
    read: false,
  },
]

const priorityIcon = {
  low: <Info className="w-4 h-4 text-blue-400" />,
  medium: <AlertTriangle className="w-4 h-4 text-orange-400" />,
  high: <AlertCircle className="w-4 h-4 text-red-400" />,
  critical: <AlertCircle className="w-4 h-4 text-red-500" />,
}

interface Props {
  open: boolean
  onClose: () => void
}

export function NotificationCenter({ open, onClose }: Props) {
  const [notifications, setNotifications] = useState<Notification[]>(MOCK_NOTIFICATIONS)

  const markAllRead = () => {
    setNotifications(prev => prev.map(n => ({ ...n, read: true })))
  }

  const markRead = (id: string) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n))
  }

  const clearAll = () => {
    setNotifications([])
  }

  const unreadCount = notifications.filter(n => !n.read).length

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40"
            onClick={onClose}
          />

          {/* Panel */}
          <motion.div
            initial={{ x: '100%', opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: '100%', opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="fixed right-0 top-0 h-full w-80 z-50 bg-gray-900 border-l border-white/[0.08] shadow-2xl flex flex-col"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-4 border-b border-white/[0.06]">
              <div className="flex items-center gap-2">
                <Bell className="w-4 h-4 text-gray-400" />
                <span className="font-semibold text-gray-100">Notifications</span>
                {unreadCount > 0 && (
                  <Badge variant="default" className="text-[10px] px-1.5 py-0">
                    {unreadCount}
                  </Badge>
                )}
              </div>
              <div className="flex items-center gap-1">
                {unreadCount > 0 && (
                  <Button variant="ghost" size="sm" onClick={markAllRead} className="text-xs h-7">
                    <CheckCheck className="w-3.5 h-3.5 mr-1" /> All read
                  </Button>
                )}
                <Button variant="ghost" size="icon" onClick={onClose} className="h-7 w-7">
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {/* Notifications list */}
            <div className="flex-1 overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full gap-3 text-gray-500">
                  <Bell className="w-10 h-10 opacity-30" />
                  <p className="text-sm">No notifications</p>
                </div>
              ) : (
                <div className="divide-y divide-white/[0.04]">
                  {notifications.map(n => (
                    <button
                      key={n.id}
                      onClick={() => markRead(n.id)}
                      className={`w-full text-left px-4 py-3.5 hover:bg-white/[0.03] transition-colors ${!n.read ? 'bg-blue-500/5' : ''}`}
                    >
                      <div className="flex items-start gap-3">
                        <div className="mt-0.5 flex-shrink-0">{priorityIcon[n.priority]}</div>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-sm font-medium text-gray-100 truncate">{n.title}</span>
                            {!n.read && (
                              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 flex-shrink-0" />
                            )}
                          </div>
                          <p className="text-xs text-gray-400 leading-relaxed">{n.message}</p>
                          <p className="text-[10px] text-gray-600 mt-1">{n.time}</p>
                        </div>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            {notifications.length > 0 && (
              <div className="p-3 border-t border-white/[0.06]">
                <Button variant="ghost" className="w-full text-xs text-gray-500" onClick={clearAll}>
                  Clear all notifications
                </Button>
              </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
