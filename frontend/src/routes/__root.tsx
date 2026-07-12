import { createFileRoute, Outlet } from '@tanstack/react-router'
import { useState, useEffect } from 'react'
import { AppSidebar } from '../components/AppSidebar'
import { TopBar } from '../components/TopBar'
import { GlobalSearch } from '../components/GlobalSearch'
import { NotificationCenter } from '../components/NotificationCenter'
import { Toaster } from 'sonner'

export const Route = createFileRoute('/')({
  component: RootLayout,
})

function RootLayout() {
  const [searchOpen, setSearchOpen] = useState(false)
  const [notificationsOpen, setNotificationsOpen] = useState(false)

  // Listen for Cmd+K / Ctrl+K keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setSearchOpen((prev) => !prev)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-gray-950 text-gray-100 font-sans">
      {/* Sidebar Navigation */}
      <AppSidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full min-w-0 overflow-hidden relative">
        {/* Top Header Bar */}
        <TopBar
          onSearchOpen={() => setSearchOpen(true)}
          onNotificationsOpen={() => setNotificationsOpen(true)}
        />

        {/* Content Outlet */}
        <main className="flex-1 overflow-y-auto overflow-x-hidden p-6 bg-[#030712]">
          <Outlet />
        </main>
      </div>

      {/* Global Command Search Overlay */}
      <GlobalSearch open={searchOpen} onClose={() => setSearchOpen(false)} />

      {/* Slide-out Notification Center Panel */}
      <NotificationCenter open={notificationsOpen} onClose={() => setNotificationsOpen(false)} />

      {/* Premium Sonner Toaster */}
      <Toaster theme="dark" position="bottom-right" closeButton rsc />
    </div>
  )
}
