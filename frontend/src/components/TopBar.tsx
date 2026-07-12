import { useState } from 'react'
import { Search, Bell, User } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useLocation } from '@tanstack/react-router'
import { cn } from '../lib/utils'

interface TopBarProps {
  onSearchOpen?: () => void
  onNotificationsOpen?: () => void
}

const routeLabels: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/vehicles': 'Vehicles',
  '/drivers': 'Drivers',
  '/trips': 'Trips',
  '/tracking': 'Live Tracking',
  '/analytics': 'Analytics',
  '/assistant': 'AI Assistant',
  '/predictions': 'ML Predictions',
  '/customer-tracking': 'Customer Tracking',
}

export function TopBar({ onSearchOpen, onNotificationsOpen }: TopBarProps) {
  const location = useLocation()
  const [notifCount] = useState(3)
  const pageTitle = routeLabels[location.pathname] ?? 'TransitOps'

  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-white/[0.06] bg-gray-950/80 backdrop-blur-sm flex-shrink-0">
      {/* Page title */}
      <AnimatePresence mode="wait">
        <motion.h1
          key={location.pathname}
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 4 }}
          transition={{ duration: 0.15 }}
          className="text-base font-semibold text-gray-100"
        >
          {pageTitle}
        </motion.h1>
      </AnimatePresence>

      {/* Right actions */}
      <div className="flex items-center gap-2">
        {/* Search */}
        <button
          onClick={onSearchOpen}
          className={cn(
            'hidden md:flex items-center gap-2 h-8 px-3 rounded-lg border border-white/[0.08] bg-white/[0.03]',
            'text-gray-500 text-xs hover:text-gray-300 hover:border-white/[0.12] transition-all duration-150'
          )}
        >
          <Search className="w-3.5 h-3.5" />
          <span>Search...</span>
          <span className="ml-1 rounded border border-white/10 bg-white/[0.05] px-1 py-0.5 text-[10px] font-mono">
            ⌘K
          </span>
        </button>

        {/* Notifications */}
        <button
          onClick={onNotificationsOpen}
          className="relative h-8 w-8 rounded-lg border border-white/[0.08] bg-white/[0.03] flex items-center justify-center text-gray-400 hover:text-gray-200 hover:border-white/[0.12] transition-all duration-150"
        >
          <Bell className="w-4 h-4" />
          {notifCount > 0 && (
            <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-blue-600 text-[9px] font-bold text-white flex items-center justify-center">
              {notifCount}
            </span>
          )}
        </button>

        {/* User avatar */}
        <button className="h-8 w-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white shadow-lg">
          <User className="w-4 h-4" />
        </button>
      </div>
    </header>
  )
}
