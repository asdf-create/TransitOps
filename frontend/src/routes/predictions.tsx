import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../lib/api'

export const Route = createFileRoute('/predictions')({
  component: Predictions,
})

function Predictions() {
  const [activeTab, setActiveTab] = useState('delay')
  const [vehicleId, setVehicleId] = useState(1)
  const [driverId, setDriverId] = useState(1)
  const [source, setSource] = useState('Warehouse A')
  const [destination, setDestination] = useState('Warehouse B')
  const [distance, setDistance] = useState(50)
  const [duration, setDuration] = useState(60)

  const delayMutation = useMutation({
    mutationFn: () => api.post('/ml/predict-delay', {
      vehicle_id: vehicleId,
      driver_id: driverId,
      source,
      destination,
      planned_distance: distance,
      planned_duration: duration
    })
  })

  const etaMutation = useMutation({
    mutationFn: () => api.post('/ml/estimate-eta', {
      vehicle_id: vehicleId,
      driver_id: driverId,
      source,
      destination,
      current_location_lat: 40.7128,
      current_location_lon: -74.0060,
      destination_lat: 40.7589,
      destination_lon: -73.9851
    })
  })

  const driverMutation = useMutation({
    mutationFn: () => api.post('/ml/recommend-drivers', {
      trip_distance: distance,
      trip_duration: duration,
      cargo_weight: 3000,
      source,
      destination
    })
  })

  const vehicleMutation = useMutation({
    mutationFn: () => api.post('/ml/recommend-vehicles', {
      cargo_weight: 3000,
      cargo_type: 'General',
      trip_distance: distance,
      source,
      destination
    })
  })

  const handlePredict = () => {
    if (activeTab === 'delay') {
      delayMutation.mutate()
    } else if (activeTab === 'eta') {
      etaMutation.mutate()
    } else if (activeTab === 'drivers') {
      driverMutation.mutate()
    } else if (activeTab === 'vehicles') {
      vehicleMutation.mutate()
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">ML Predictions</h2>
      
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex space-x-4 mb-6 border-b">
            {['delay', 'eta', 'drivers', 'vehicles'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 font-medium ${
                  activeTab === tab
                    ? 'border-b-2 border-blue-600 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Vehicle ID</label>
              <input
                type="number"
                value={vehicleId}
                onChange={(e) => setVehicleId(Number(e.target.value))}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Driver ID</label>
              <input
                type="number"
                value={driverId}
                onChange={(e) => setDriverId(Number(e.target.value))}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Source</label>
              <input
                type="text"
                value={source}
                onChange={(e) => setSource(e.target.value)}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Destination</label>
              <input
                type="text"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Distance (km)</label>
              <input
                type="number"
                value={distance}
                onChange={(e) => setDistance(Number(e.target.value))}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Duration (min)</label>
              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
          </div>
          
          <button
            onClick={handlePredict}
            disabled={delayMutation.isPending || etaMutation.isPending || driverMutation.isPending || vehicleMutation.isPending}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400"
          >
            Generate Prediction
          </button>
        </div>
      </div>
      
      <div className="mt-6 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Results</h3>
          
          {activeTab === 'delay' && delayMutation.data && (
            <div className="space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-900 mb-2">Delay Prediction</h4>
                <p className="text-2xl font-bold text-blue-700">{delayMutation.data.predicted_delay_minutes} minutes</p>
                <p className="text-sm text-blue-600">Delay probability: {(delayMutation.data.delay_probability * 100).toFixed(1)}%</p>
                <p className="text-sm text-blue-600">On-time probability: {(delayMutation.data.on_time_probability * 100).toFixed(1)}%</p>
                <p className="text-sm text-blue-600">Confidence: {(delayMutation.data.confidence * 100).toFixed(1)}%</p>
              </div>
              <div>
                <h4 className="font-semibold mb-2">Delay Factors:</h4>
                <ul className="list-disc list-inside text-gray-600">
                  {delayMutation.data.delay_factors.map((factor: string, index: number) => (
                    <li key={index}>{factor}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
          
          {activeTab === 'eta' && etaMutation.data && (
            <div className="space-y-4">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 className="font-semibold text-green-900 mb-2">ETA Estimation</h4>
                <p className="text-2xl font-bold text-green-700">{etaMutation.data.estimated_duration_minutes} minutes</p>
                <p className="text-sm text-green-600">Confidence: {(etaMutation.data.confidence * 100).toFixed(1)}%</p>
                <p className="text-sm text-green-600">Traffic factor: {etaMutation.data.traffic_factor}</p>
                <p className="text-sm text-green-600">Weather factor: {etaMutation.data.weather_factor}</p>
              </div>
            </div>
          )}
          
          {activeTab === 'drivers' && driverMutation.data && (
            <div className="space-y-4">
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <h4 className="font-semibold text-purple-900 mb-2">Driver Recommendations</h4>
                <p className="text-sm text-purple-600">{driverMutation.data.reasoning}</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {driverMutation.data.recommended_drivers.map((driver: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-semibold">{driver.name}</h4>
                      <span className="bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded-full">
                        {driver.match_score * 100}% match
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 space-y-1">
                      <p>Safety Score: {driver.safety_score}/100</p>
                      <p>Experience: {driver.experience_years} years</p>
                      <p>Total Trips: {driver.total_trips}</p>
                      <p>Status: {driver.availability}</p>
                      <p>Rating: {driver.rating}/5.0</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {activeTab === 'vehicles' && vehicleMutation.data && (
            <div className="space-y-4">
              <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                <h4 className="font-semibold text-orange-900 mb-2">Vehicle Recommendations</h4>
                <p className="text-sm text-orange-600">{vehicleMutation.data.reasoning}</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {vehicleMutation.data.recommended_vehicles.map((vehicle: any, index: number) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-semibold">{vehicle.registration}</h4>
                      <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full">
                        {vehicle.match_score * 100}% match
                      </span>
                    </div>
                    <div className="text-sm text-gray-600 space-y-1">
                      <p>Type: {vehicle.type}</p>
                      <p>Model: {vehicle.model}</p>
                      <p>Capacity: {vehicle.capacity_kg} kg</p>
                      <p>Fuel Efficiency: {vehicle.fuel_efficiency_km_l} km/l</p>
                      <p>Maintenance Score: {vehicle.maintenance_score}/100</p>
                      <p>Status: {vehicle.status}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {(delayMutation.isPending || etaMutation.isPending || driverMutation.isPending || vehicleMutation.isPending) && (
            <div className="text-center py-8 text-gray-500">Generating predictions...</div>
          )}
        </div>
      </div>
      
      <div className="mt-6 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">ML Capabilities</h3>
          <div className="text-sm text-gray-600">
            <p>• <strong>Delay Prediction:</strong> Predict trip delays based on route characteristics, traffic patterns, and historical data</p>
            <p>• <strong>ETA Estimation:</strong> Calculate accurate arrival times considering traffic, weather, and route complexity</p>
            <p>• <strong>Driver Recommendations:</strong> Suggest optimal drivers based on safety scores, experience, and availability</p>
            <p>• <strong>Vehicle Recommendations:</strong> Recommend vehicles based on capacity, efficiency, and maintenance status</p>
            <p className="mt-2 text-orange-600">Note: All predictions use synthetic data patterns for demonstration purposes.</p>
          </div>
        </div>
      </div>
    </div>
  )
}