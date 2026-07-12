import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

export const Route = createFileRoute('/analytics')({
  component: Analytics,
})

function Analytics() {
  const { data: revenue, isLoading: revenueLoading } = useQuery({
    queryKey: ['analytics-revenue'],
    queryFn: () => api.get('/analytics/revenue'),
  })

  const { data: fuelEfficiency, isLoading: fuelLoading } = useQuery({
    queryKey: ['analytics-fuel'],
    queryFn: () => api.get('/analytics/fuel-efficiency'),
  })

  const { data: driverRankings, isLoading: driversLoading } = useQuery({
    queryKey: ['analytics-drivers'],
    queryFn: () => api.get('/analytics/driver-rankings'),
  })

  const { data: vehicleRoi, isLoading: roiLoading } = useQuery({
    queryKey: ['analytics-roi'],
    queryFn: () => api.get('/analytics/vehicle-roi'),
  })

  if (revenueLoading || fuelLoading || driversLoading || roiLoading) {
    return (
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Analytics</h2>
        <div className="text-gray-500">Loading...</div>
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Analytics</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Revenue Analytics</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Revenue</span>
                <span className="font-semibold text-green-600">${revenue?.total_revenue?.toFixed(2) || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average Revenue/Trip</span>
                <span className="font-semibold">${revenue?.average_revenue_per_trip?.toFixed(2) || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Trips</span>
                <span className="font-semibold">{revenue?.total_trips || 0}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Fuel Efficiency</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Average Fleet Efficiency</span>
                <span className="font-semibold">{fuelEfficiency?.average_fleet_efficiency?.toFixed(2) || 0} km/l</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Vehicles Tracked</span>
                <span className="font-semibold">{fuelEfficiency?.vehicle_count || 0}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Top Drivers</h3>
            <div className="space-y-2">
              {driverRankings?.slice(0, 5).map((driver: any, index: number) => (
                <div key={driver.driver_id} className="flex justify-between items-center">
                  <span className="text-gray-600">{index + 1}. {driver.name}</span>
                  <span className="font-semibold text-blue-600">{driver.safety_score}/100</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Vehicle ROI</h3>
            <div className="space-y-2">
              {Object.entries(vehicleRoi || {}).slice(0, 5).map(([registration, data]: [string, any]) => (
                <div key={registration} className="flex justify-between items-center">
                  <span className="text-gray-600">{registration}</span>
                  <span className={`font-semibold ${data.roi_percentage >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {data.roi_percentage.toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 flex justify-end">
        <button 
          onClick={() => window.open('http://localhost:8000/analytics/export/csv')}
          className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700"
        >
          Export CSV
        </button>
      </div>
    </div>
  )
}
