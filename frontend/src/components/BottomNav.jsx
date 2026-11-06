import { NavLink } from 'react-router-dom'

const NAV_ITEMS = [
  { path: '/', label: 'Overview', icon: 'dashboard' },
  { path: '/open-pit', label: 'Open-Pit', icon: 'landscape' },
  { path: '/underground', label: 'Predictions', icon: 'insights' },
  { path: '/alerts', label: 'Alerts', icon: 'warning' },
  { path: '/settings', label: 'Settings', icon: 'tune' },
]

export default function BottomNav() {
  return (
    <nav className="fixed bottom-0 w-full z-50 pb-safe bg-surface/90 backdrop-blur-xl shadow-[0_-1px_12px_rgba(0,0,0,0.4)]">
      <div className="flex justify-around items-center h-20 px-gutter">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex flex-col items-center justify-center gap-1 w-16 h-16 transition-colors ${
                isActive
                  ? 'text-primary font-bold'
                  : 'text-on-surface-variant hover:text-on-surface'
              }`
            }
          >
            <span className="material-symbols-outlined text-[22px]">{item.icon}</span>
            {item.path === '/alerts' && (
              <span className="absolute top-2 right-3 w-2 h-2 rounded-full bg-primary-container animate-pulse" />
            )}
            <span className="font-label-sm text-label-sm">{item.label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  )
}