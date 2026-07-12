import { Link, useLocation } from '@tanstack/react-router'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard,
  Truck,
  Users,
  Route,
  MapPin,
  BarChart3,
  Bot,
  Brain,
  ChevronLeft,
  ChevronRight,
  Zap,
} from 'lucide-react'
import { useState } from 'react'
import { cn } from '../lib/utils'
import { Tooltip, TooltipContent, TooltipTrigger, TooltipProvider } from './ui/tooltip'

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/vehicles', icon: Truck, label: 'Vehicles' },
  { to: '/drivers', icon: Users, label: 'Drivers' },
  { to: '/trips', icon: Route, label: 'Trips' },
  { to: '/tracking', icon: MapPin, label: 'Live Tracking' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/assistant', icon: Bot, label: 'AI Assistant' },
  { to: '/predictions', icon: Brain, label: 'ML Predictions' },
  { to: '/customer-tracking', icon: Zap, label: 'Customer Tracking' },
]

export function AppSidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  return (
    <TooltipProvider delayDuration={100}>
      <motion.aside
        animate={{ width: collapsed ? 64 : 220 }}
        transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
        className="flex-shrink-0 flex flex-col h-screen bg-gray-950 border-r border-white/[0.06] relative z-20"
      >
        {/* Logo */}
        <div className="flex items-center h-14 px-4 border-b border-white/[0.06]">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-blue-600/30">
              <Truck className="w-4 h-4 text-white" />
            </div>
            <AnimatePresence>
              {!collapsed && (
                <motion.span
                  initial={{ opacity: 0, width: 0 }}
                  animate={{ opacity: 1, width: 'auto' }}
                  exit={{ opacity: 0, width: 0 }}
                  transition={{ duration: 0.2 }}
                  className="font-bold text-gray-100 text-sm whitespace-nowrap overflow-hidden"
                >
                  TransitOps
                </motion.span>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Nav items */}
        <nav className="flex-1 py-4 px-2 space-y-0.5 overflow-y-auto overflow-x-hidden">
          {navItems.map(({ to, icon: Icon, label }) => {
            const active = location.pathname === to || location.pathname.startsWith(to + '/')
            return (
              <Tooltip key={to}>
                <TooltipTrigger asChild>
                  <Link
                    to={to}
                    className={cn(
                      'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group relative',
                      active
                        ? 'bg-blue-600/15 text-blue-400 border border-blue-500/20'
                        : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.05]'
                    )}
                  >
                    {active && (
                      <motion.div
                        layoutId="sidebar-indicator"
                        className="absolute inset-0 rounded-lg bg-blue-600/10 border border-blue-500/20"
                        transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
                      />
                    )}
                    <Icon
                      className={cn(
                        'w-4 h-4 flex-shrink-0 relative z-10',
                        active ? 'text-blue-400' : 'text-gray-500 group-hover:text-gray-300'
                      )}
                    />
                    <AnimatePresence>
                      {!collapsed && (
                        <motion.span
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          exit={{ opacity: 0 }}
                          transition={{ duration: 0.15 }}
                          className="relative z-10 whitespace-nowrap overflow-hidden"
                        >
                          {label}
                        </motion.span>
                      )}
                    </AnimatePresence>
                  </Link>
                </TooltipTrigger>
                {collapsed && (
                  <TooltipContent side="right">
                    {label}
                  </TooltipContent>
                )}
              </Tooltip>
            )
          })}
        </nav>

        {/* Collapse toggle */}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="flex items-center justify-center h-12 w-full border-t border-white/[0.06] text-gray-500 hover:text-gray-300 hover:bg-white/[0.04] transition-colors"
        >
          {collapsed ? (
            <ChevronRight className="w-4 h-4" />
          ) : (
            <ChevronLeft className="w-4 h-4" />
          )}
        </button>
      </motion.aside>
    </TooltipProvider>
  )
}
