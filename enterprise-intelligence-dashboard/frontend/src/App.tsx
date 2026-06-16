import { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  TrendingUp, 
  Activity, 
  Briefcase, 
  Users,
  ShieldAlert,
  ArrowUpRight,
  ArrowDownRight,
  CircleDollarSign,
  PackageSearch
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

// Mock trend data for charts
const mockTrendData = [
  { name: 'Jan', revenue: 65000 },
  { name: 'Feb', revenue: 59000 },
  { name: 'Mar', revenue: 80000 },
  { name: 'Apr', revenue: 81000 },
  { name: 'May', revenue: 95000 },
  { name: 'Jun', revenue: 105000 },
  { name: 'Jul', revenue: 125000 },
];

export default function App() {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // In a real app, this fetches from the FastAPI backend
  useEffect(() => {
    setTimeout(() => {
      setDashboardData({
        kpis: {
          enterprise_score: 87.5,
          revenue_growth: { value: 15.2, current_revenue: 125000, previous_revenue: 108500 },
          inventory_turnover: { value: 4.5 },
          conversion_rate: { value: 24.5 },
          cash_flow_health: { value: 1.2 }
        },
        insights: [
          { type: "Executive", priority: "Low", message: "All KPIs are within healthy thresholds. Maintain current operations." },
          { type: "Sales & CRM", priority: "Medium", message: "Consider reviewing Lead conversion strategy as growth has plateaued." }
        ]
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const { kpis, insights } = dashboardData;

  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      {/* Sidebar Navigation */}
      <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-800 tracking-tight flex items-center gap-2">
            <Activity className="text-blue-600" />
            EID Analytics
          </h1>
          <p className="text-xs text-gray-500 mt-1">SME Executive Portal</p>
        </div>
        <div className="flex-1 py-4">
          <nav className="space-y-1 px-3">
            {[
              { name: 'Executive Overview', icon: LayoutDashboard, active: true },
              { name: 'Sales Intelligence', icon: TrendingUp, active: false },
              { name: 'Operations Intelligence', icon: PackageSearch, active: false },
              { name: 'Customer Intelligence', icon: Users, active: false },
              { name: 'Executive Insights', icon: Briefcase, active: false },
            ].map((item) => (
              <a
                key={item.name}
                href="#"
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  item.active 
                    ? 'bg-blue-50 text-blue-700' 
                    : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                }`}
              >
                <item.icon className={`w-5 h-5 ${item.active ? 'text-blue-600' : 'text-gray-400'}`} />
                {item.name}
              </a>
            ))}
          </nav>
        </div>
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm">
              EX
            </div>
            <div>
              <p className="text-sm font-medium text-gray-700">Executive User</p>
              <p className="text-xs text-gray-500">Board Member</p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <header className="bg-white border-b border-gray-200 px-8 py-5 flex justify-between items-center sticky top-0 z-10">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Executive Overview</h2>
            <p className="text-sm text-gray-500 mt-0.5">High-level snapshot of business health and operational metrics</p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-500">Last updated: Today, 08:30 AM</span>
            <button className="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-50 shadow-sm transition-all">
              Download Report
            </button>
          </div>
        </header>

        <main className="p-8 max-w-7xl mx-auto space-y-8">
          {/* Top Level KPIs */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Enterprise Intelligence Score */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between overflow-hidden relative group">
              <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-blue-50 to-white rounded-bl-full -z-10 transition-transform group-hover:scale-110"></div>
              <div>
                <p className="text-sm font-medium text-gray-500 flex items-center gap-2">
                  Enterprise Score
                  <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
                </p>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-4xl font-bold text-gray-900">{kpis.enterprise_score}</span>
                  <span className="text-sm font-medium text-gray-500">/ 100</span>
                </div>
              </div>
              <div className="mt-4 w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${kpis.enterprise_score}%` }}></div>
              </div>
            </div>

            {/* Revenue */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500 flex justify-between items-center">
                  Total Revenue (YTD)
                  <CircleDollarSign className="w-5 h-5 text-gray-400" />
                </p>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-gray-900">${(kpis.revenue_growth.current_revenue / 1000).toFixed(1)}k</span>
                </div>
              </div>
              <div className="mt-4 flex items-center gap-1.5 text-sm font-medium text-green-600 bg-green-50 w-fit px-2 py-1 rounded-md">
                <ArrowUpRight className="w-4 h-4" />
                {kpis.revenue_growth.value}% from last month
              </div>
            </div>

            {/* Cash Flow */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500 flex justify-between items-center">
                  Cash Flow Ratio
                  <Activity className="w-5 h-5 text-gray-400" />
                </p>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-gray-900">{kpis.cash_flow_health.value}x</span>
                </div>
              </div>
              <div className="mt-4 flex items-center gap-1.5 text-sm font-medium text-green-600 bg-green-50 w-fit px-2 py-1 rounded-md">
                <ArrowUpRight className="w-4 h-4" />
                Healthy liquidity
              </div>
            </div>

            {/* Conversion */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500 flex justify-between items-center">
                  Lead Conversion
                  <Users className="w-5 h-5 text-gray-400" />
                </p>
                <div className="mt-2 flex items-baseline gap-2">
                  <span className="text-3xl font-bold text-gray-900">{kpis.conversion_rate.value}%</span>
                </div>
              </div>
              <div className="mt-4 flex items-center gap-1.5 text-sm font-medium text-red-600 bg-red-50 w-fit px-2 py-1 rounded-md">
                <ArrowDownRight className="w-4 h-4" />
                -2.1% from last month
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Chart Area */}
            <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h3 className="text-lg font-bold text-gray-800">Revenue Trajectory</h3>
                  <p className="text-sm text-gray-500">Historical performance vs targets</p>
                </div>
                <select className="text-sm border border-gray-300 rounded-md px-3 py-1.5 text-gray-700 bg-white">
                  <option>Last 6 Months</option>
                  <option>Year to Date</option>
                  <option>12 Months Rolling</option>
                </select>
              </div>
              <div className="h-72 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={mockTrendData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#6b7280', fontSize: 12}} dy={10} />
                    <YAxis axisLine={false} tickLine={false} tick={{fill: '#6b7280', fontSize: 12}} tickFormatter={(value) => `$${value/1000}k`} />
                    <Tooltip 
                      contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                      formatter={(value: number) => [`$${value.toLocaleString()}`, 'Revenue']}
                    />
                    <Area type="monotone" dataKey="revenue" stroke="#2563eb" strokeWidth={3} fillOpacity={1} fill="url(#colorRevenue)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* AI Insights Panel */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col">
              <div className="p-6 border-b border-gray-100">
                <h3 className="text-lg font-bold text-gray-800 flex items-center gap-2">
                  <ShieldAlert className="w-5 h-5 text-amber-500" />
                  Decision Support
                </h3>
                <p className="text-sm text-gray-500 mt-1">Automated operational insights</p>
              </div>
              <div className="p-6 flex-1 overflow-y-auto space-y-4">
                {insights.map((insight: any, idx: number) => (
                  <div key={idx} className={`p-4 rounded-lg border ${
                    insight.priority === 'High' || insight.priority === 'Critical' 
                      ? 'bg-red-50 border-red-100 text-red-800' 
                      : insight.priority === 'Medium' 
                        ? 'bg-amber-50 border-amber-100 text-amber-800'
                        : 'bg-green-50 border-green-100 text-green-800'
                  }`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold uppercase tracking-wider opacity-80">{insight.type}</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                        insight.priority === 'High' || insight.priority === 'Critical' 
                          ? 'bg-red-200 text-red-900' 
                          : insight.priority === 'Medium' 
                            ? 'bg-amber-200 text-amber-900'
                            : 'bg-green-200 text-green-900'
                      }`}>
                        {insight.priority}
                      </span>
                    </div>
                    <p className="text-sm font-medium leading-relaxed">{insight.message}</p>
                  </div>
                ))}

                <div className="p-4 rounded-lg border bg-blue-50 border-blue-100 text-blue-800">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold uppercase tracking-wider opacity-80">Inventory</span>
                    <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-blue-200 text-blue-900">Optimization</span>
                  </div>
                  <p className="text-sm font-medium leading-relaxed">Turnover is stable at {kpis.inventory_turnover.value}x. Next procurement cycle recommended on 15th.</p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
