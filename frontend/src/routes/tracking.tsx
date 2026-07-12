import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { api } from '../lib/api'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import { Skeleton } from '../components/ui/skeleton'
import { MapPin, RefreshCw, Truck } from 'lucide-react'
import { motion } from 'framer-motion'

export const Route = createFileRoute('/tracking')({
  component: Tracking,
})

function Tracking() {
  const map = useRef<maplibregl.Map | null>(null)
  const markersRef = useRef<maplibregl.Marker[]>([])

  const { data: vehicleLocations, isLoading, refetch } = useQuery({
    queryKey: ['vehicle-locations'],
    queryFn: () => api.get('/tracking/vehicles'),
    refetchInterval: 5000, // Auto refresh locations every 5s
  })

  // Helper to draw markers
  const updateMarkers = () => {
    if (!map.current || !vehicleLocations) return

    // Remove existing markers
    markersRef.current.forEach(marker => marker.remove())
    markersRef.current = []

    // Add new markers for each vehicle
    vehicleLocations.forEach((location: any) => {
      if (location.latitude !== 0 || location.longitude !== 0) {
        const marker = new maplibregl.Marker({ color: '#3b82f6' })
          .setLngLat([location.longitude, location.latitude])
          .setPopup(new maplibregl.Popup({ offset: 25 }).setHTML(`
            <div class="p-2 text-gray-900">
              <h3 class="font-bold text-xs">${location.registration_number}</h3>
              <p class="text-[10px] mt-0.5">Status: <span class="font-semibold">${location.status}</span></p>
              <p class="text-[10px]">Speed: <span class="font-semibold">${location.speed || 0} km/h</span></p>
            </div>
          `))
          .addTo(map.current!)
        
        markersRef.current.push(marker)
      }
    })

    // Fit map to show all markers
    if (markersRef.current.length > 0) {
      const bounds = new maplibregl.LngLatBounds()
      markersRef.current.forEach(marker => {
        const lngLat = marker.getLngLat()
        bounds.extend([lngLat.lng, lngLat.lat])
      })
      map.current.fitBounds(bounds, { padding: 50, maxZoom: 8 })
    }
  }

  // Trigger update when locations change
  useEffect(() => {
    updateMarkers()
  }, [vehicleLocations])

  // Callback ref to safely initialize map when container mounts in the DOM
  const mapContainerRef = (el: HTMLDivElement | null) => {
    if (!el) {
      if (map.current) {
        map.current.remove()
        map.current = null
      }
      return
    }

    if (map.current) return // Already initialized

    map.current = new maplibregl.Map({
      container: el,
      style: 'https://demotiles.maplibre.org/style.json',
      center: [78.9629, 20.5937], // Centered on India by default
      zoom: 4,
    })

    map.current.addControl(new maplibregl.NavigationControl(), 'top-right')

    // Initial draw once map is ready
    map.current.on('load', () => {
      updateMarkers()
    })
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <Skeleton className="h-8 w-48 bg-white/5" />
          <Skeleton className="h-9 w-24 bg-white/5" />
        </div>
        <Skeleton className="h-[450px] w-full bg-white/5 rounded-xl" />
        <Skeleton className="h-[200px] w-full bg-white/5 rounded-xl" />
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-gray-100 flex items-center gap-2">
            <MapPin className="w-5 h-5 text-blue-400" />
            <span>Live Tracking Control Room</span>
          </h2>
          <p className="text-xs text-gray-400">Real-time GPS status and positioning of all active fleet vehicles.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span>Auto-refreshing</span>
          </div>
          <button
            onClick={() => refetch()}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-xs text-gray-300 hover:bg-white/[0.06] transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Map panel */}
      <Card className="bg-white/[0.01] border-white/[0.06] overflow-hidden">
        <CardContent className="p-0 h-[450px] relative">
          <div ref={mapContainerRef} className="w-full h-full" />
        </CardContent>
      </Card>

      {/* Active vehicles grid */}
      <Card className="bg-white/[0.01] border-white/[0.06]">
        <CardHeader className="border-b border-white/[0.06] py-3.5">
          <CardTitle className="text-sm font-semibold text-gray-200">Active Transit Assets</CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          {vehicleLocations && vehicleLocations.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {vehicleLocations.map((location: any) => (
                <div key={location.vehicle_id} className="border border-white/[0.06] bg-white/[0.01] rounded-xl p-4 hover:border-blue-500/20 transition-all">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <Truck className="w-4 h-4 text-blue-400" />
                      <h4 className="font-semibold text-xs text-gray-200">{location.registration_number}</h4>
                    </div>
                    <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full ${
                      location.status === 'On Trip' 
                        ? 'bg-blue-500/10 border border-blue-500/20 text-blue-400' 
                        : 'bg-gray-500/10 border border-gray-500/20 text-gray-400'
                    }`}>
                      {location.status}
                    </span>
                  </div>
                  <div className="text-[11px] text-gray-400 space-y-1 mt-3">
                    <div className="flex justify-between">
                      <span>Current Speed:</span>
                      <span className="text-gray-200 font-medium">{location.speed || 0} km/h</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Compass Heading:</span>
                      <span className="text-gray-200 font-medium">{location.heading || 0}°</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-6 text-xs text-gray-500">
              No active vehicles are currently in transit.
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  )
}
