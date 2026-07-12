import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { motion } from 'framer-motion'
import ReactECharts from 'echarts-for-react'
import { Truck, Users, Route, Percent, RefreshCw, Calendar } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card'
import { Skeleton } from '../components/ui/skeleton'

export const Route = createFileRoute('/dashboard')({
  component: Dashboard,
})

function Dashboard() {
  const { data: kpis, isLoading: kpisLoading, refetch: refetchKpis } = useQuery({
    queryKey: ['dashboard-kpis'],
    queryFn: () => api.get('/dashboard/kpis'),
  })

  const { data: fleetStatus, isLoading: fleetLoading } = useQuery({
    queryKey: ['dashboard-fleet-status'],
    queryFn: () => api.get('/dashboard/fleet-status'),
  })

  const { data: driverStatus, isLoading: driverLoading } = useQuery({
    queryKey: ['dashboard-driver-status'],
    queryFn: () => api.get('/dashboard/driver-status'),
  })

  const { data: recentActivity, isLoading: activityLoading } = useQuery({
    queryKey: ['dashboard-recent-activity'],
    queryFn: () => api.get('/dashboard/recent-activity?limit=5'),
  })

  const handleRefresh = () => {
    refetchKpis()
  }

  const isLoading = kpisLoading || fleetLoading || driverLoading || activityLoading

  // ECharts Pie option for Fleet Status
  const getFleetChartOption = () => {
    if (!fleetStatus) return {}
    const data = [
      { value: fleetStatus.available || 0, name: 'Available', itemStyle: { color: '#10b981' } },
      { value: fleetStatus.on_trip || 0, name: 'On Trip', itemStyle: { color: '#3b82f6' } },
      { value: fleetStatus.in_shop || 0, name: 'In Shop', itemStyle: { color: '#f97316' } },
      { value: fleetStatus.retired || 0, name: 'Retired', itemStyle: { color: '#6b7280' } },
    ]
    return {
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
      legend: { bottom: '0%', textStyle: { color: '#9ca3af' } },
      series: [
        {
          name: 'Fleet Status',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: { borderRadius: 6, borderColor: '#111827', borderWidth: 2 },
          label: { show: false },
          emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold', color: '#f3f4f6' } },
          data,
        },
      ],
    }
  }

  // ECharts Bar option for Driver Status
  const getDriverChartOption = () => {
    if (!driverStatus) return {}
    const categories = ['Available', 'On Trip', 'Off Duty', 'Suspended']
    const data = [
      driverStatus.available || 0,
      driverStatus.on_trip || 0,
      driverStatus.off_duty || 0,
      driverStatus.suspended || 0,
    ]
    return {
      backgroundColor: 'transparent',
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      xAxis: {
        type: 'category',
        data: categories,
        axisLabel: { color: '#9ca3af' },
        axisLine: { lineStyle: { color: '#374151' } },
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#9ca3af' },
        splitLine: { lineStyle: { color: '#1f2937' } },
      },
      series: [
        {
          data,
          type: 'bar',
          barWidth: '40%',
          itemStyle: {
            color: '#3b82f6',
            borderRadius: [4, 4, 0, 0],
          },
        },
      ],
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <Skeleton className="h-8 w-48 bg-white/5" />
          <Skeleton className="h-9 w-24 bg-white/5" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-28 bg-white/5 rounded-xl" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Skeleton className="h-80 bg-white/5 rounded-xl" />
          <Skeleton className="h-80 bg-white/5 rounded-xl" />
        </div>
      </div>
    )
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.08 },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 12 },
    show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 100 } },
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="show"
      className="space-y-6"
    >
      {/* Header bar */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-gray-100">Operations Control Room</h2>
          <p className="text-xs text-gray-400">Real-time status of TransitOps logistics</p>
        </div>
        <button
          onClick={handleRefresh}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] text-xs text-gray-300 hover:bg-white/[0.06] transition-all"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Control Room</span>
        </button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div variants={itemVariants}>
          <Card className="bg-white/[0.02] border-white/[0.06] hover:border-blue-500/20 hover:bg-white/[0.04] transition-all duration-200">
            <CardContent className="p-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-gray-400">Total Active Vehicles</p>
                <h3 className="text-2xl font-bold text-gray-100 mt-1">
                  {kpis?.vehicles?.total || 0}
                </h3>
                <p className="text-[10px] text-emerald-400 mt-0.5">
                  {kpis?.vehicles?.available || 0} currently available
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <Truck className="w-5 h-5" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="bg-white/[0.02] border-white/[0.06] hover:border-emerald-500/20 hover:bg-white/[0.04] transition-all duration-200">
            <CardContent className="p-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-gray-400">Active Operators</p>
                <h3 className="text-2xl font-bold text-gray-100 mt-1">
                  {kpis?.drivers?.total || 0}
                </h3>
                <p className="text-[10px] text-emerald-400 mt-0.5">
                  {kpis?.drivers?.available || 0} ready for dispatch
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
                <Users className="w-5 h-5" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="bg-white/[0.02] border-white/[0.06] hover:border-purple-500/20 hover:bg-white/[0.04] transition-all duration-200">
            <CardContent className="p-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-gray-400">Active Shipments</p>
                <h3 className="text-2xl font-bold text-gray-100 mt-1">
                  {kpis?.trips?.active || 0}
                </h3>
                <p className="text-[10px] text-purple-400 mt-0.5">
                  {kpis?.trips?.completed || 0} shipments completed
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
                <Route className="w-5 h-5" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="bg-white/[0.02] border-white/[0.06] hover:border-orange-500/20 hover:bg-white/[0.04] transition-all duration-200">
            <CardContent className="p-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-medium text-gray-400">Fleet Efficiency</p>
                <h3 className="text-2xl font-bold text-gray-100 mt-1">
                  {kpis?.metrics?.fleet_utilization?.toFixed(1) || 0}%
                </h3>
                <p className="text-[10px] text-orange-400 mt-0.5">
                  Average safety: {kpis?.metrics?.average_safety_score?.toFixed(0) || 0}
                </p>
              </div>
              <div className="w-10 h-10 rounded-lg bg-orange-500/10 border border-orange-500/20 flex items-center justify-center text-orange-400">
                <Percent className="w-5 h-5" />
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div variants={itemVariants}>
          <Card className="bg-white/[0.02] border-white/[0.06]">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold text-gray-200">Fleet Status Distribution</CardTitle>
            </CardHeader>
            <CardContent className="h-72">
              <ReactECharts option={getFleetChartOption()} style={{ height: '100%' }} />
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={itemVariants}>
          <Card className="bg-white/[0.02] border-white/[0.06]">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold text-gray-200">Operator Duty Distribution</CardTitle>
            </CardHeader>
            <CardContent className="h-72">
              <ReactECharts option={getDriverChartOption()} style={{ height: '100%' }} />
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Activity feed */}
      <motion.div variants={itemVariants}>
        <Card className="bg-white/[0.02] border-white/[0.06]">
          <CardHeader className="border-b border-white/[0.06] py-3.5">
            <CardTitle className="text-sm font-semibold text-gray-200">Recent Completed Shipments</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            {recentActivity && recentActivity.length > 0 ? (
              <div className="divide-y divide-white/[0.04]">
                {recentActivity.map((activity: any, idx: number) => (
                  <div key={idx} className="flex items-center justify-between p-4 hover:bg-white/[0.01]">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded bg-blue-500/10 flex items-center justify-center text-blue-400 text-xs">
                        <Route className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="text-xs font-semibold text-gray-200">
                          Shipment {activity.tracking_id} Complete
                        </p>
                        <p className="text-[10px] text-gray-400">
                          Driver: {activity.driver} | Vehicle: {activity.vehicle}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 text-gray-400 text-[10px]">
                      <Calendar className="w-3 h-3" />
                      <span>{new Date(activity.timestamp).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-6 text-center text-xs text-gray-500">
                No recent shipment activities found.
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  )
}
