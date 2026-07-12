import { createFileRoute } from '@tanstack/react-router'
import { useState, useEffect, useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { api } from '../lib/api'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Clock, User, Truck, MapPin, Calendar, Navigation, RefreshCw } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Skeleton } from '../components/ui/skeleton'

export const Route = createFileRoute('/customer-tracking')({
  component: CustomerTracking,
})

function CustomerTracking() {
  const [trackingId, setTrackingId] = useState('')
  const [activeTrackingId, setActiveTrackingId] = useState<string | null>(null)
  
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<maplibregl.Map | null>(null)
  const markerRef = useRef<maplibregl.Marker | null>(null)
  const routeLayerAdded = useRef<boolean>(false)

  // 1. Fetch Tracking Details
  const { data: details, isLoading: detailsLoading, error: detailsError, refetch } = useQuery({
    queryKey: ['tracking-details', activeTrackingId],
    queryFn: () => api.get(`/tracking/${activeTrackingId}`),
    enabled: !!activeTrackingId,
    refetchInterval: 10000, // refresh location every 10s
  })

  // 2. Fetch Route Coordinates
  const { data: routeData } = useQuery({
    queryKey: ['tracking-route', activeTrackingId],
    queryFn: () => api.get(`/tracking/${activeTrackingId}/route`),
    enabled: !!activeTrackingId,
  })

  // 3. Fetch Timeline History
  const { data: historyData } = useQuery({
    queryKey: ['tracking-history', activeTrackingId],
    queryFn: () => api.get(`/tracking/${activeTrackingId}/history`),
    enabled: !!activeTrackingId,
  })

  // Parse query parameter if present on load
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const tid = params.get('tracking_id')
    if (tid) {
      setTrackingId(tid)
      setActiveTrackingId(tid)
    }
  }, [])

  // Initialize Map
  useEffect(() => {
    if (!mapContainer.current || !activeTrackingId || map.current) return

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: 'https://demotiles.maplibre.org/style.json',
      center: [78.9629, 20.5937], // Centered on India by default
      zoom: 4,
    })

    map.current.addControl(new maplibregl.NavigationControl(), 'top-right')

    return () => {
      if (map.current) {
        map.current.remove()
        map.current = null
        routeLayerAdded.current = false
      }
    }
  }, [activeTrackingId])

  // Update vehicle position marker and draw route line
  useEffect(() => {
    if (!map.current || !details) return

    const { latitude, longitude, vehicle_registration, current_status } = details

    // Draw / update marker position
    if (markerRef.current) {
      markerRef.current.setLngLat([longitude, latitude])
    } else {
      markerRef.current = new maplibregl.Marker({ color: '#2563eb' })
        .setLngLat([longitude, latitude])
        .setPopup(new maplibregl.Popup({ offset: 25 }).setHTML(`
          <div style="color: #1f2937; padding: 4px;">
            <p style="font-weight: bold; margin: 0;">${vehicle_registration}</p>
            <p style="font-size: 11px; margin: 2px 0 0 0;">${current_status}</p>
          </div>
        `))
        .addTo(map.current)
    }

    // Centering camera
    map.current.easeTo({ center: [longitude, latitude], zoom: 6 })

    // Draw route geometry if loaded
    if (routeData && routeData.coordinates && routeData.coordinates.length > 0) {
      const geojson = {
        type: 'Feature',
        properties: {},
        geometry: {
          type: 'LineString',
          coordinates: routeData.coordinates,
        },
      }

      if (map.current.isStyleLoaded()) {
        const sourceId = 'route-source'
        const layerId = 'route-layer'

        if (map.current.getSource(sourceId)) {
          (map.current.getSource(sourceId) as maplibregl.GeoJSONSource).setData(geojson as any)
        } else {
          map.current.addSource(sourceId, {
            type: 'geojson',
            data: geojson as any,
          })

          map.current.addLayer({
            id: layerId,
            type: 'line',
            source: sourceId,
            layout: {
              'line-join': 'round',
              'line-cap': 'round',
            },
            paint: {
              'line-color': '#3b82f6',
              'line-width': 4,
              'line-opacity': 0.6,
            },
          })
          routeLayerAdded.current = true
        }
      }
    }
  }, [details, routeData])

  const handleTrackSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!trackingId.trim()) return
    const cleanId = trackingId.trim().toUpperCase()
    setActiveTrackingId(cleanId)
    // Update URL query param silently
    const newurl = `${window.location.protocol}//${window.location.host}${window.location.pathname}?tracking_id=${cleanId}`
    window.history.pushState({ path: newurl }, '', newurl)
  }

  const handleReset = () => {
    setActiveTrackingId(null)
    setTrackingId('')
    const newurl = `${window.location.protocol}//${window.location.host}${window.location.pathname}`
    window.history.pushState({ path: newurl }, '', newurl)
    if (map.current) {
      map.current.remove()
      map.current = null
      routeLayerAdded.current = false
    }
    markerRef.current = null
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center">
        <h2 className="text-xl font-bold text-gray-100 flex items-center justify-center gap-2">
          <Navigation className="w-5 h-5 text-blue-400 animate-pulse" />
          <span>Customer Delivery Portal</span>
        </h2>
        <p className="text-xs text-gray-400">Enter your tracking ID for real-time delivery tracking.</p>
      </div>

      {/* Tracking Input Panel */}
      <Card className="bg-white/[0.01] border-white/[0.06] p-6">
        <form onSubmit={handleTrackSubmit} className="flex gap-3">
          <Input
            value={trackingId}
            onChange={(e) => setTrackingId(e.target.value)}
            placeholder="Enter tracking ID (e.g. TRK-410283)"
            className="flex-1 bg-white/[0.02] border-white/[0.08] focus-visible:ring-blue-500/50 text-xs h-10"
          />
          <Button
            type="submit"
            className="bg-blue-600 hover:bg-blue-500 text-white font-semibold px-6 h-10 text-xs"
          >
            Locate Shipment
          </Button>
          {activeTrackingId && (
            <Button
              type="button"
              variant="outline"
              onClick={handleReset}
              className="border-white/[0.08] text-gray-300 hover:bg-white/[0.04] h-10 text-xs"
            >
              Clear
            </Button>
          )}
        </form>
      </Card>

      {/* Results view */}
      <AnimatePresence mode="wait">
        {activeTrackingId && (
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 15 }}
            className="space-y-6"
          >
            {detailsLoading ? (
              <div className="space-y-4">
                <Skeleton className="h-44 bg-white/5 rounded-xl" />
                <Skeleton className="h-64 bg-white/5 rounded-xl" />
              </div>
            ) : detailsError || !details ? (
              <Card className="bg-white/[0.01] border-red-500/20 p-8 text-center space-y-3">
                <div className="text-red-400 text-3xl">📦</div>
                <h3 className="text-sm font-bold text-gray-200">Shipment Details Unavailable</h3>
                <p className="text-xs text-gray-400">
                  We couldn't locate tracking ID "{activeTrackingId}". Please verify and try again.
                </p>
              </Card>
            ) : (
              <div className="space-y-6">
                {/* Status overview */}
                <Card className="bg-white/[0.01] border-white/[0.06] p-6 space-y-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Tracking Reference</p>
                      <h3 className="text-lg font-bold text-gray-100">{details.tracking_id}</h3>
                    </div>
                    <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${
                      details.current_status === 'Delivered'
                        ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                        : details.current_status === 'Cancelled'
                        ? 'bg-red-500/10 border-red-500/20 text-red-400'
                        : 'bg-blue-500/10 border-blue-500/20 text-blue-400 animate-pulse'
                    }`}>
                      {details.current_status}
                    </span>
                  </div>

                  {/* Progress Indicator */}
                  <div className="space-y-1">
                    <div className="flex justify-between text-[10px] text-gray-400 font-semibold uppercase">
                      <span>Transit Progress</span>
                      <span>{details.progress_percentage.toFixed(0)}%</span>
                    </div>
                    <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-600 rounded-full transition-all duration-500"
                        style={{ width: `${details.progress_percentage}%` }}
                      />
                    </div>
                  </div>

                  {/* Route points */}
                  <div className="grid grid-cols-2 gap-6 text-xs border-t border-white/[0.06] pt-4">
                    <div>
                      <p className="text-[10px] text-gray-400 font-semibold uppercase">Source</p>
                      <p className="text-gray-200 font-bold mt-0.5">{details.source}</p>
                    </div>
                    <div>
                      <p className="text-[10px] text-gray-400 font-semibold uppercase">Destination</p>
                      <p className="text-gray-200 font-bold mt-0.5">{details.destination}</p>
                    </div>
                  </div>
                </Card>

                {/* Map Panel */}
                <Card className="bg-white/[0.01] border-white/[0.06] overflow-hidden">
                  <CardHeader className="py-3 px-6 border-b border-white/[0.06] flex flex-row items-center justify-between">
                    <CardTitle className="text-xs font-semibold text-gray-200">Live Delivery Route</CardTitle>
                    <button onClick={() => refetch()} className="text-gray-400 hover:text-gray-200">
                      <RefreshCw className="w-3.5 h-3.5" />
                    </button>
                  </CardHeader>
                  <CardContent className="p-0 h-80 relative">
                    <div ref={mapContainer} className="w-full h-full" />
                  </CardContent>
                </Card>

                {/* Delivery details & Timeline */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Delivery Info */}
                  <Card className="bg-white/[0.01] border-white/[0.06] p-6 space-y-4">
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Asset Assignments</h4>
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                          <Truck className="w-4 h-4" />
                        </div>
                        <div>
                          <p className="text-[10px] text-gray-400 uppercase font-semibold">Vehicle</p>
                          <p className="text-xs font-semibold text-gray-200">
                            {details.vehicle_name} ({details.vehicle_registration})
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded bg-emerald-600/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                          <User className="w-4 h-4" />
                        </div>
                        <div>
                          <p className="text-[10px] text-gray-400 uppercase font-semibold">Assigned Operator</p>
                          <p className="text-xs font-semibold text-gray-200">{details.driver_name}</p>
                        </div>
                      </div>
                      {details.estimated_arrival && (
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded bg-purple-600/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                            <Clock className="w-4 h-4" />
                          </div>
                          <div>
                            <p className="text-[10px] text-gray-400 uppercase font-semibold">Estimated Arrival</p>
                            <p className="text-xs font-semibold text-gray-200">
                              {new Date(details.estimated_arrival).toLocaleString()}
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  </Card>

                  {/* Timeline History */}
                  <Card className="bg-white/[0.01] border-white/[0.06] p-6">
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4">Milestone Tracker</h4>
                    <div className="relative border-l border-white/[0.06] pl-4 space-y-4">
                      {historyData && historyData.events ? (
                        historyData.events.map((event: any, idx: number) => (
                          <div key={idx} className="relative">
                            <div className="absolute -left-[21px] mt-1.5 w-2.5 h-2.5 rounded-full border border-blue-500 bg-gray-950" />
                            <div>
                              <p className="text-xs font-bold text-gray-200">{event.status}</p>
                              <p className="text-[10px] text-gray-400 mt-0.5">{event.description}</p>
                              <span className="text-[9px] text-gray-500 block mt-0.5">
                                {new Date(event.timestamp).toLocaleString()}
                              </span>
                            </div>
                          </div>
                        ))
                      ) : (
                        <div className="text-xs text-gray-500">Timeline events loading...</div>
                      )}
                    </div>
                  </Card>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}