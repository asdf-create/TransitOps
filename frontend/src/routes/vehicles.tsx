import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/vehicles')({
  component: Vehicles,
})

function Vehicles() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Vehicles</h2>
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Vehicle Registry</h3>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
              Add Vehicle
            </button>
          </div>
          <div className="text-gray-500 text-sm">
            <p>Vehicle management will be connected to the backend API.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
