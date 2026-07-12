import { createFileRoute } from '@tanstack/react-router'
import { useEffect, useRef, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'
import { api } from '../lib/api'

export const Route = createFileRoute('/tracking')({
  component: Tracking,
})

function Tracking() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<maplibregl.Map | null>(null)
  const markersRef = useRef<maplibregl.Marker[]>([])
  const { data: vehicleLocations, isLoading } = useQuery({
    queryKey: ['vehicle-locations'],
    queryFn: () => api.get('/tracking/vehicles'),
    refetchInterval: 5000,
  })

  useEffect(() => {
    if (!mapContainer.current || map.current) return

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: 'https://demotiles.maplibre.org/style.json',
      center: [0, 20],
      zoom: 2,
    })

    map.current.addControl(new maplibregl.NavigationControl(), 'top-right')

    return () => {
      map.current?.remove()
    }
  }, [])

  useEffect(() => {
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
            <div class="p-2">
              <h3 class="font-bold">${location.registration_number}</h3>
              <p class="text-sm">Status: ${location.status}</p>
              <p class="text-sm">Speed: ${location.speed || 0} km/h</p>
            </div>
          `))
          .addTo(map.current)
        
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
      map.current.fitBounds(bounds, { padding: 50 })
    }
  }, [vehicleLocations])

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Live Tracking</h2>
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Vehicle Locations</h3>
            <div className="flex space-x-2">
              <button 
                onClick={() => window.location.reload()}
                className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
              >
                Refresh
              </button>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-sm text-gray-600">Auto-refreshing</span>
              </div>
            </div>
          </div>
          {isLoading ? (
            <div className="text-gray-500 text-center py-8">Loading vehicle locations...</div>
          ) : (
            <div ref={mapContainer} className="w-full h-96 rounded-lg" />
          )}
        </div>
      </div>
      
      <div className="mt-6 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Active Vehicles</h3>
          {isLoading ? (
            <div className="text-gray-500">Loading...</div>
          ) : vehicleLocations && vehicleLocations.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {vehicleLocations.map((location: any) => (
                <div key={location.vehicle_id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold">{location.registration_number}</h4>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      location.status === 'On Trip' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {location.status}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600 space-y-1">
                    <p>Speed: {location.speed || 0} km/h</p>
                    <p>Heading: {location.heading || 0}°</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-gray-500">No active vehicles on trips</div>
          )}
        </div>
      </div>
    </div>
  )
}
