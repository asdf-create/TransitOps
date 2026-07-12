import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/analytics')({
  component: Analytics,
})

function Analytics() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Analytics</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Revenue Analytics</h3>
            <div className="text-gray-500 text-sm">
              <p>Revenue charts will be displayed here using Apache ECharts.</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Fuel Efficiency</h3>
            <div className="text-gray-500 text-sm">
              <p>Fuel efficiency analytics will be displayed here.</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Driver Rankings</h3>
            <div className="text-gray-500 text-sm">
              <p>Driver performance rankings will be displayed here.</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Vehicle ROI</h3>
            <div className="text-gray-500 text-sm">
              <p>Vehicle ROI calculations will be displayed here.</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-6 flex justify-end">
        <button className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700">
          Export CSV
        </button>
      </div>
    </div>
  )
}
