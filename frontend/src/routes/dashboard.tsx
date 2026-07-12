import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard')({
  component: Dashboard,
})

function Dashboard() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold">
                  V
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Vehicles</dt>
                  <dd className="text-3xl font-semibold text-gray-900">--</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold">
                  D
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Total Drivers</dt>
                  <dd className="text-3xl font-semibold text-gray-900">--</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-purple-500 flex items-center justify-center text-white font-bold">
                  T
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Active Trips</dt>
                  <dd className="text-3xl font-semibold text-gray-900">--</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-orange-500 flex items-center justify-center text-white font-bold">
                  %
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">Fleet Utilization</dt>
                  <dd className="text-3xl font-semibold text-gray-900">--%</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-8 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Activity</h3>
          <div className="text-gray-500 text-sm">
            <p>Dashboard will be populated with real data from the backend API.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
