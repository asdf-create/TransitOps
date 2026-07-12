import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { api } from '../lib/api'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Clock, ShieldAlert, Award, Star, Truck, Users, Settings } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'

export const Route = createFileRoute('/predictions')({
  component: Predictions,
})

function Predictions() {
  const [activeTab, setActiveTab] = useState<'delay' | 'eta' | 'drivers' | 'vehicles'>('delay')
  const [vehicleId, setVehicleId] = useState(1)
  const [driverId, setDriverId] = useState(1)
  const [source, setSource] = useState('Mumbai')
  const [destination, setDestination] = useState('Pune')
  const [distance, setDistance] = useState(150)
  const [duration, setDuration] = useState(180)
  const [cargoWeight, setCargoWeight] = useState(3000)

  const delayMutation = useMutation({
    mutationFn: () =>
      api.post('/ml/predict-delay', {
        vehicle_id: vehicleId,
        driver_id: driverId,
        source,
        destination,
        planned_distance: distance,
        planned_duration: duration,
      }),
  })

  const etaMutation = useMutation({
    mutationFn: () =>
      api.post('/ml/estimate-eta', {
        vehicle_id: vehicleId,
        driver_id: driverId,
        source,
        destination,
        current_location_lat: 19.076,
        current_location_lon: 72.8777,
        destination_lat: 18.5204,
        destination_lon: 73.8567,
      }),
  })

  const driverMutation = useMutation({
    mutationFn: () =>
      api.post('/ml/recommend-drivers', {
        trip_distance: distance,
        trip_duration: duration,
        cargo_weight: cargoWeight,
        source,
        destination,
      }),
  })

  const vehicleMutation = useMutation({
    mutationFn: () =>
      api.post('/ml/recommend-vehicles', {
        cargo_weight: cargoWeight,
        cargo_type: 'General',
        trip_distance: distance,
        source,
        destination,
      }),
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

  const isPending =
    delayMutation.isPending ||
    etaMutation.isPending ||
    driverMutation.isPending ||
    vehicleMutation.isPending

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-xl font-bold text-gray-100 flex items-center gap-2">
          <Brain className="w-5 h-5 text-blue-400" />
          <span>Machine Learning Intelligence</span>
        </h2>
        <p className="text-xs text-gray-400">
          Predictive analytics powered by local pre-trained XGBoost and LightGBM modules.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Form Panel */}
        <Card className="bg-white/[0.01] border-white/[0.06] p-6 lg:col-span-1 space-y-4">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
            Trip Specifications
          </h3>

          <div className="space-y-3">
            <div>
              <label className="text-[10px] font-semibold text-gray-400 uppercase">Source Location</label>
              <Input
                value={source}
                onChange={(e) => setSource(e.target.value)}
                className="bg-white/[0.02] border-white/[0.08] focus-visible:ring-blue-500/50 mt-1 h-9 text-xs"
              />
            </div>
            <div>
              <label className="text-[10px] font-semibold text-gray-400 uppercase">Destination</label>
              <Input
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                className="bg-white/[0.02] border-white/[0.08] focus-visible:ring-blue-500/50 mt-1 h-9 text-xs"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] font-semibold text-gray-400 uppercase">Distance (km)</label>
                <Input
                  type="number"
                  value={distance}
                  onChange={(e) => setDistance(Number(e.target.value))}
                  className="bg-white/[0.02] border-white/[0.08] focus-visible:ring-blue-500/50 mt-1 h-9 text-xs"
                />
              </div>
              <div>
                <label className="text-[10px] font-semibold text-gray-400 uppercase">Duration (mins)</label>
                <Input
                  type="number"
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  className="bg-white/[0.02] border-white/[0.08] focus-visible:ring-blue-500/50 mt-1 h-9 text-xs"
                />
              </div>
            </div>
            <div>
              <label className="text-[10px] font-semibold text-gray-400 uppercase">Cargo Weight (kg)</label>
              <Input
                type="number"
                value={cargoWeight}
                onChange={(e) => setCargoWeight(Number(e.target.value))}
                className="bg-white/[0.02] border-white/[0.08] focus-visible:ring-blue-500/50 mt-1 h-9 text-xs"
              />
            </div>

            <div className="pt-2">
              <Button
                onClick={handlePredict}
                disabled={isPending}
                className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs h-9"
              >
                {isPending ? 'Computing Inference...' : 'Run ML Prediction'}
              </Button>
            </div>
          </div>
        </Card>

        {/* Right Tabbed Results Panel */}
        <div className="lg:col-span-2 space-y-4">
          {/* Tab Selector */}
          <div className="flex border-b border-white/[0.06] p-1 bg-white/[0.01] rounded-lg">
            {(['delay', 'eta', 'drivers', 'vehicles'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 py-2 text-center text-xs font-semibold rounded-md transition-all duration-150 ${
                  activeTab === tab
                    ? 'bg-blue-600/15 text-blue-400 border border-blue-500/20'
                    : 'text-gray-400 hover:text-gray-200'
                }`}
              >
                {tab === 'delay'
                  ? 'Delay Risk'
                  : tab === 'eta'
                  ? 'Live ETA'
                  : tab === 'drivers'
                  ? 'Best Drivers'
                  : 'Best Vehicles'}
              </button>
            ))}
          </div>

          {/* Tab Content Panels */}
          <Card className="bg-white/[0.01] border-white/[0.06] p-6 min-h-[300px] flex flex-col justify-center">
            <AnimatePresence mode="wait">
              {activeTab === 'delay' && (
                <motion.div
                  key="delay"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="space-y-6"
                >
                  {delayMutation.data ? (
                    <div className="space-y-6">
                      <div className="flex justify-between items-center">
                        <div>
                          <h4 className="text-sm font-bold text-gray-200">Trip Delay Analysis</h4>
                          <p className="text-[10px] text-gray-400">Confidence: {(delayMutation.data.confidence * 100).toFixed(0)}%</p>
                        </div>
                        <div className={`px-2.5 py-1 rounded-full text-[10px] font-bold border ${
                          delayMutation.data.delay_probability > 0.6
                            ? 'bg-red-500/10 border-red-500/20 text-red-400'
                            : delayMutation.data.delay_probability > 0.3
                            ? 'bg-orange-500/10 border-orange-500/20 text-orange-400'
                            : 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                        }`}>
                          {(delayMutation.data.delay_probability * 100).toFixed(0)}% Delay Risk
                        </div>
                      </div>

                      {/* Progress Bar Gauge */}
                      <div className="space-y-1">
                        <div className="flex justify-between text-[10px] text-gray-400 font-semibold uppercase">
                          <span>Delay Risk Level</span>
                          <span>{(delayMutation.data.delay_probability * 100).toFixed(0)}%</span>
                        </div>
                        <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full transition-all duration-300 ${
                              delayMutation.data.delay_probability > 0.6
                                ? 'bg-red-500'
                                : delayMutation.data.delay_probability > 0.3
                                ? 'bg-orange-500'
                                : 'bg-emerald-500'
                            }`}
                            style={{ width: `${delayMutation.data.delay_probability * 100}%` }}
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-white/[0.01] border border-white/[0.04] p-3 rounded-lg">
                          <p className="text-[10px] text-gray-400 uppercase font-semibold">Predicted Delay</p>
                          <p className="text-lg font-bold text-gray-200 mt-1">
                            {delayMutation.data.predicted_delay_minutes} minutes
                          </p>
                        </div>
                        <div className="bg-white/[0.01] border border-white/[0.04] p-3 rounded-lg">
                          <p className="text-[10px] text-gray-400 uppercase font-semibold">On-Time Probability</p>
                          <p className="text-lg font-bold text-emerald-400 mt-1">
                            {(delayMutation.data.on_time_probability * 100).toFixed(0)}%
                          </p>
                        </div>
                      </div>

                      {/* Contributing Factors */}
                      <div className="space-y-2">
                        <h5 className="text-[10px] font-bold text-gray-400 uppercase">Primary Delay Risk Factors</h5>
                        <div className="flex flex-wrap gap-2">
                          {delayMutation.data.delay_factors.map((factor: string, idx: number) => (
                            <div key={idx} className="flex items-center gap-1.5 px-2.5 py-1 rounded border border-white/[0.05] bg-white/[0.02] text-[10px] text-gray-300">
                              <ShieldAlert className="w-3.5 h-3.5 text-orange-400" />
                              <span>{factor}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-12 text-xs text-gray-500">
                      Specify parameters on the left and click "Run ML Prediction" to see delay analysis.
                    </div>
                  )}
                </motion.div>
              )}

              {activeTab === 'eta' && (
                <motion.div
                  key="eta"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="space-y-6"
                >
                  {etaMutation.data ? (
                    <div className="space-y-6">
                      <div>
                        <h4 className="text-sm font-bold text-gray-200">ML-Enhanced ETA Prediction</h4>
                        <p className="text-[10px] text-gray-400">Confidence: {(etaMutation.data.confidence * 100).toFixed(0)}%</p>
                      </div>

                      <div className="grid grid-cols-2 gap-4">
                        <div className="bg-white/[0.01] border border-white/[0.04] p-4 rounded-lg flex items-center gap-3">
                          <Clock className="w-6 h-6 text-blue-400" />
                          <div>
                            <p className="text-[10px] text-gray-400 uppercase font-semibold">Predicted Arrival Time</p>
                            <p className="text-base font-bold text-gray-200 mt-0.5">
                              {new Date(etaMutation.data.estimated_arrival).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </p>
                          </div>
                        </div>
                        <div className="bg-white/[0.01] border border-white/[0.04] p-4 rounded-lg flex items-center gap-3">
                          <Settings className="w-6 h-6 text-emerald-400" />
                          <div>
                            <p className="text-[10px] text-gray-400 uppercase font-semibold">Remaining Travel Time</p>
                            <p className="text-base font-bold text-gray-200 mt-0.5">
                              {etaMutation.data.estimated_duration_minutes} minutes
                            </p>
                          </div>
                        </div>
                      </div>

                      <div className="border-t border-white/[0.06] pt-4 space-y-2">
                        <p className="text-[10px] text-gray-400 font-bold uppercase">Simulated Trip Environment</p>
                        <div className="flex gap-4 text-xs">
                          <span className="text-gray-300">Traffic Modifier: <strong className="text-blue-400">{etaMutation.data.traffic_factor}x</strong></span>
                          <span className="text-gray-300">Weather Modifier: <strong className="text-blue-400">{etaMutation.data.weather_factor}x</strong></span>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-12 text-xs text-gray-500">
                      Specify parameters and run prediction to estimate ML arrival times.
                    </div>
                  )}
                </motion.div>
              )}

              {activeTab === 'drivers' && (
                <motion.div
                  key="drivers"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="space-y-4"
                >
                  {driverMutation.data ? (
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-sm font-bold text-gray-200">Recommended Fleet Operators</h4>
                        <p className="text-[10px] text-gray-400">{driverMutation.data.reasoning}</p>
                      </div>

                      <div className="space-y-2">
                        {driverMutation.data.recommended_drivers.map((driver: any, idx: number) => (
                          <div key={idx} className="flex items-center justify-between p-3 border border-white/[0.04] bg-white/[0.01] hover:bg-white/[0.03] rounded-lg transition-all">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-full bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400 text-xs">
                                <Award className="w-4 h-4" />
                              </div>
                              <div>
                                <p className="text-xs font-semibold text-gray-200">{driver.name}</p>
                                <p className="text-[10px] text-gray-400">
                                  Safety: {driver.safety_score}% • Experience: {driver.experience_years} yrs • Status: {driver.availability}
                                </p>
                              </div>
                            </div>
                            <div className="text-right">
                              <span className="text-[10px] text-blue-400 font-bold bg-blue-500/10 border border-blue-500/20 px-2 py-0.5 rounded">
                                {(driver.match_score * 100).toFixed(0)}% Match
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-12 text-xs text-gray-500">
                      Click predict to run the driver recommendation classifier.
                    </div>
                  )}
                </motion.div>
              )}

              {activeTab === 'vehicles' && (
                <motion.div
                  key="vehicles"
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -10 }}
                  className="space-y-4"
                >
                  {vehicleMutation.data ? (
                    <div className="space-y-4">
                      <div>
                        <h4 className="text-sm font-bold text-gray-200">Recommended Fleet Assets</h4>
                        <p className="text-[10px] text-gray-400">{vehicleMutation.data.reasoning}</p>
                      </div>

                      <div className="space-y-2">
                        {vehicleMutation.data.recommended_vehicles.map((vehicle: any, idx: number) => (
                          <div key={idx} className="flex items-center justify-between p-3 border border-white/[0.04] bg-white/[0.01] hover:bg-white/[0.03] rounded-lg transition-all">
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded bg-emerald-600/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 text-xs">
                                <Truck className="w-4 h-4" />
                              </div>
                              <div>
                                <p className="text-xs font-semibold text-gray-200">{vehicle.registration}</p>
                                <p className="text-[10px] text-gray-400">
                                  {vehicle.manufacturer} {vehicle.model} • Capacity: {vehicle.capacity_kg} kg • Status: {vehicle.status}
                                </p>
                              </div>
                            </div>
                            <div className="text-right">
                              <span className="text-[10px] text-emerald-400 font-bold bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                                {(vehicle.match_score * 100).toFixed(0)}% Match
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-12 text-xs text-gray-500">
                      Click predict to run the vehicle suitability classifier.
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </Card>
        </div>
      </div>
    </div>
  )
}