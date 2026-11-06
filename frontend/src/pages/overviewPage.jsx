import { useState } from 'react'

const DEMO_KPIS = [
  { label: 'Total Records', value: '1,247', status: 'success' },
  { label: 'Active Alerts', value: '3', status: 'error' },
  { label: 'System Status', value: 'Operational', status: 'success' },
  { label: 'Last Analyzed', value: '2 min ago', status: 'success' },
]

const RISK_DATA = [
  { name: 'Safe', value: 85 },
  { name: 'Risk', value: 15 },
]

const SECTORS = [
  'Sector 1',
  'Sector 2',
  'Sector 3',
  'Sector 4',
  'Sector 5',
]

const MINING_EVENTS = [
  { id: 1, time: '14:18', type: 'Crown Pillar', severity: 'critical' },
  { id: 2, time: '13:42', type: 'Hanging Wall', severity: 'warning' },
  { id: 3, time: '12:11', type: 'Stress Redistribution', severity: 'nominal' },
]

export default function OverviewPage() {
  const [activeView, setActiveView] = useState('sector-1')

  return (
    <div className="pb-8">
      <section className="shadow-sm">
        <span className="w-1.5 h-1.5 rounded-full bg-tertiary animate-pulse-dot shrink-0" />
        <span className="font-label-sm text-label-sm text-on-surface uppercase tracking-wider">SENSOR FEED</span>
      </section>
      <section className="shadow-sm p-2">
        <h1 className="scada-page-title">GeoAlert AI</h1>
        <p className="scada-page-subtitle">Monitoring</p>
        <button className="scada-btn-primary">
          <span className="material-symbols-outlined">refresh</span>Refresh
        </button>
      </section>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-2">
        {DEMO_KPIS.map((kpi) => (
          <div key={kpi.label} className="scada-card">
            <span>{kpi.label}</span><span>{kpi.value}</span>
          </div>
        ))}
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-2 mt-2">
        <div><h3>Risk</h3><p>Safe 85% / Risk 15%</p></div>
        <div><h3>Sectors</h3><p>{SECTORS.map(s => <button key={s}>{s}</button>)}</p></div>
        <div><h3>Open-Pit</h3><p>Critical conditions</p></div>
      </div>
      <div className="scada-card mt-2">
        <h3>Recent Events</h3>
        {MINING_EVENTS.map(e => (
          <div key={e.id} className="p-2 rounded">
            <span>{e.type}</span><span>{e.time}</span>
          </div>
        ))}
      </div>
    </div>
  )
}