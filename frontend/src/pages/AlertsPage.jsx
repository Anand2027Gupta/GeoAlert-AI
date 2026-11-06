import { useState } from 'react'

const DEMO_ALERTS = [
  { id: 1, timestamp: '2026-10-28 14:18:02', recipient: 'safety@mine.com', phone: '+91-98765-43210', method: 'SMTP/SMS', status: '250 OK', statusType: 'success', severity: 'Critical', type: 'Critical' },
  { id: 2, timestamp: '2026-10-28 13:42:55', recipient: 'engineer@mine.com', phone: '+91-98765-43211', method: 'Email', status: '250 OK', statusType: 'success', severity: 'High', type: 'FS Alert' },
  { id: 3, timestamp: '2026-10-28 12:11:18', recipient: 'supervisor@mine.com', phone: '+91-98765-43212', method: 'SMS', status: '250 OK', statusType: 'success', severity: 'Moderate', type: 'Reinforcement Alert' },
]

const SEVERITIES = ['All', 'Critical', 'High', 'Moderate', 'Info']
const TYPES = ['Critical', 'FS Alert', 'Reinforcement Alert', 'Energy Alert', 'Peak Energy Alert', 'Info']
const METHODS = ['Email', 'SMS', 'App Notification', 'None']

export default function AlertsPage() {
  const [severityFilter, setSeverityFilter] = useState('All')
  const [typeFilter, setTypeFilter] = useState(['Critical'])
  const [notificationMethod, setNotificationMethod] = useState('Email')
  const [recipient, setRecipient] = useState('')
  const [subject, setSubject] = useState('')
  const [message, setMessage] = useState('')
  const [formSubmitted, setFormSubmitted] = useState(false)

  const filteredAlerts = DEMO_ALERTS.filter(a => {
    if (severityFilter !== 'All' && a.severity !== severityFilter) return false
    if (typeFilter.length > 0 && !typeFilter.includes(a.type)) return false
    return true
  })

  return (
    <div className="flex flex-col w-full pb-8">
      <section className="bg-surface-container-lowest px-gutter py-space-xs text-on-surface-variant shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-y-1 gap-x-2">
          <div className="flex items-center gap-1.5 min-w-0">
            <span className="w-2 h-2 rounded-full bg-secondary-container/20 text-secondary animate-pulse-dot shrink-0" />
            <span className="font-label-sm text-label-sm uppercase tracking-wider text-secondary truncate">
              SMTP: DEMO — NOT CONNECTED
            </span>
          </div>
          <div className="flex items-center gap-1.5 shrink-0">
            <span className="material-symbols-outlined text-secondary text-[14px]">cell_tower</span>
            <span className="font-label-sm text-label-sm text-secondary">SMS MODEM — DEMO</span>
          </div>
        </div>
      </section>
      <section className="px-gutter pt-space-md pb-space-sm bg-surface-container-low shadow-sm">
        <div className="flex items-start justify-between gap-space-sm">
          <div className="min-w-0">
            <div className="flex items-center gap-1.5 mb-1">
              <span className="px-1.5 py-0.5 rounded bg-error-container text-on-error-container font-label-sm text-label-sm uppercase tracking-widest font-bold">
                3 ACTIVE ALERTS
              </span>
            </div>
            <h1 className="scada-page-title">Alerts & Notifications</h1>
            <p className="scada-page-subtitle">Monitor high-risk stability events with intelligent filtering and classification.</p>
          </div>
        </div>
      </section>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-space-md">
        <div className="lg:col-span-2">
          <div className="scada-card">
            <div className="scada-section-header">
              <div className="flex items-center gap-space-xs">
                <span className="material-symbols-outlined text-secondary text-[18px]">crisis_alert</span>
                <span className="font-label-sm text-label-sm uppercase font-bold text-on-surface tracking-wider">Alert Log</span>
              </div>
              <div className="flex gap-space-xs">
                <select className="scada-select" value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
                  {SEVERITIES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            </div>
            <div className="overflow-y-auto max-h-96">
              <table className="scada-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Recipient</th>
                    <th>Method</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredAlerts.map((alert) => (
                    <tr key={alert.id} className="hover:bg-surface-container-high/40 transition-colors">
                      <td className="py-2.5 px-space-sm font-label-sm text-label-sm text-on-surface whitespace-nowrap">
                        {alert.timestamp}
                      </td>
                      <td className="py-2.5 px-space-sm min-w-0">
                        <span className="font-body-sm text-body-sm text-on-surface font-medium truncate block">{alert.recipient}</span>
                        <span className="font-label-sm text-[9px] text-on-surface-variant block truncate">{alert.phone}</span>
                      </td>
                      <td className="py-2.5 px-space-sm whitespace-nowrap">
                        <span className="px-1.5 py-0.5 rounded bg-surface-container text-secondary font-label-sm text-[10px] uppercase font-bold">
                          {alert.method}
                        </span>
                      </td>
                      <td className="py-2.5 px-space-sm text-right whitespace-nowrap">
                        <span className="inline-flex items-center gap-1 text-tertiary font-label-sm text-label-sm font-semibold">
                          <span className={`w-1.5 h-1.5 rounded-full bg-${alert.statusType === 'success' ? 'tertiary' : 'error'}`}></span>
                          {alert.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="scada-card">
            <h3 className="font-label-md text-label-md text-on-surface mb-space-sm">Send Notification</h3>
            <p className="font-body-sm text-[11px] text-on-surface-variant mb-space-sm">
              Demo mode — no actual notification will be sent. SMTP/SMS not connected.
            </p>
            <div className="space-y-space-sm">
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant block mb-space-xs">Recipient Email(s)</label>
                <input
                  type="text"
                  className="scada-input"
                  placeholder="e.g. safety@mine.com, engineer@mine.com"
                  value={recipient}
                  onChange={(e) => setRecipient(e.target.value)}
                />
              </div>
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant block mb-space-xs">Subject</label>
                <input
                  type="text"
                  className="scada-input"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                />
              </div>
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant block mb-space-xs">Message</label>
                <textarea
                  className="scada-input"
                  rows={3}
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />
              </div>
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant block mb-space-xs">Notification Method</label>
                <select className="scada-select" value={notificationMethod} onChange={(e) => setNotificationMethod(e.target.value)}>
                  {METHODS.map(m => <option key={m} value={m}>{m}</option>)}
                </select>
              </div>
              <button
                className="scada-btn-primary w-full"
                onClick={() => {
                  setFormSubmitted(true)
                  setTimeout(() => setFormSubmitted(false), 3000)
                }}
                disabled={formSubmitted}
              >
                {formSubmitted ? 'Demo — Not Connected' : 'Send Notification (Demo)'}
              </button>
            </div>
          </div>

          <div className="scada-card mt-space-md">
            <h3 className="font-label-md text-label-md text-on-surface mb-space-sm">Filters</h3>
            <div className="space-y-space-sm">
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant block mb-space-xs uppercase tracking-wider">Severity Filter</label>
                <select className="scada-select" value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
                  {SEVERITIES.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="font-label-sm text-label-sm text-on-surface-variant block mb-space-xs uppercase tracking-wider">Type Filter</label>
                <select className="scada-select" multiple value={typeFilter} onChange={(e) => {
                  const selected = Array.from(e.target.selectedOptions).map(o => o.value)
                  setTypeFilter(selected)
                }}>
                  {TYPES.map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}