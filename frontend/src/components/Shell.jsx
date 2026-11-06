import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import BottomNav from './BottomNav'

const NAV_ITEMS = [
  { path: '/', label: 'Overview', icon: 'dashboard' },
  { path: '/open-pit', label: 'Open-Pit', icon: 'landscape' },
  { path: '/underground', label: 'Predictions', icon: 'insights' },
  { path: '/alerts', label: 'Alerts', icon: 'warning' },
  { path: '/settings', label: 'Settings', icon: 'tune' },
]

export default function Shell({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex flex-col h-full w-full relative">
      <header className="fixed top-0 w-full z-50 pt-safe bg-surface/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.4)]">
        <div className="h-16 px-gutter flex items-center justify-between gap-space-sm">
          <div className="flex items-center gap-space-sm">
            <button
              aria-label="Toggle Navigation Drawer"
              className="w-11 h-11 flex items-center justify-center rounded text-on-surface hover:text-primary active:bg-surface-container"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              type="button"
            >
              <span className="material-symbols-outlined text-[24px]">menu</span>
            </button>
            <img
              alt="GeoAlert AI Logo"
              className="h-8 w-auto object-contain"
              src="https://lh3.googleusercontent.com/aida/AEtjO1VmrHHBtuimom0dJKmKl0QNf7IZY0Knjw47so3IWM7SZd8E1uBjGrcXvPPGA49tTGYxb1aS9fwnrvyR5-VesOalT-YjBDresAZSUwM8BNFkFXsEgjUThzBtbDPOPXo-NFznd1DecI3goSoNEQhdMy451wjeVE8rW3tTZ3s0Xe-Kc2r-rrbrPP5uPvWvZqMRb3IbssygU88rIlypz1aTsO65WdtNQNL2Q4z71DISXAJvpLF-u8vljswP"
            />
            <div className="flex flex-col">
              <h1 className="scada-page-title uppercase">GeoAlert AI</h1>
              <span className="font-label-sm text-label-sm text-secondary uppercase tracking-wider">SCADA v4.8</span>
            </div>
          </div>
          <div className="flex items-center gap-space-xs">
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
              <span className="text-on-primary text-[18px]">person</span>
            </div>
          </div>
        </div>
      </header>
      <aside
        className={`fixed top-16 left-0 h-[calc(100vh-3.5rem)] w-72 bg-surface-container-low border-r border-outline z-40 transition-transform duration-300 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} flex flex-col`}
      >
        <div className="flex-1 overflow-y-auto p-gutter space-y-1">
          <div className="flex items-center justify-between px-space-sm py-space-xs font-label-sm text-label-sm text-on-surface">
            <span className="text-tertiary flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-tertiary animate-pulse-dot" />
              STATUS: OPERATIONAL v2.4.1
            </span>
            <span className="text-secondary font-label-sm">LAT: 42ms</span>
          </div>
          <div className="flex items-center justify-between text-on-surface-variant font-label-sm text-label-sm">
            <span>OFFLINE CACHE: READY</span>
            <span className="material-symbols-outlined text-[14px] text-tertiary">cloud_done</span>
          </div>
          <nav className="mt-space-md space-y-0.5">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center justify-between px-space-md py-space-sm rounded text-on-surface-variant hover:text-on-surface hover:bg-surface-container active:bg-surface-container-high transition-colors ${
                    isActive ? 'bg-surface-container-high text-primary font-bold' : ''
                  }`
                }
              >
                <div className="flex items-center gap-space-md">
                  <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
                  <span className="font-body-md text-body-md font-medium">{item.label}</span>
                </div>
                {item.path === '/alerts' && (
                  <span className="px-1.5 py-0.5 rounded bg-primary-container text-on-primary-container font-label-sm text-label-sm font-bold">
                    3 CRIT
                  </span>
                )}
              </NavLink>
            ))}
            <div className="pt-space-sm px-space-sm py-space-xs font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
              Data & Utilities
            </div>
            <NavLink to="/upload" className="flex items-center gap-space-md px-space-md py-space-sm rounded text-on-surface-variant hover:text-on-surface hover:bg-surface-container active:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-[20px]">upload_file</span>
              <span className="font-body-md text-body-md font-medium">Data & Uploads</span>
            </NavLink>
            <NavLink to="/reports" className="flex items-center gap-space-md px-space-md py-space-sm rounded text-on-surface-variant hover:text-on-surface hover:bg-surface-container active:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-[20px]">summarize</span>
              <span className="font-body-md text-body-md font-medium">Reports & Analytics</span>
            </NavLink>
            <NavLink to="/help-desk" className="flex items-center gap-space-md px-space-md py-space-sm rounded text-on-surface-variant hover:text-on-surface hover:bg-surface-container active:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-[20px]">support_agent</span>
              <span className="font-body-md text-body-md font-medium">Help Desk</span>
            </NavLink>
            <NavLink to="/settings" className="flex items-center gap-space-md px-space-md py-space-sm rounded text-on-surface-variant hover:text-on-surface hover:bg-surface-container active:bg-surface-container-high transition-colors">
              <span className="material-symbols-outlined text-[20px]">settings</span>
              <span className="font-body-md text-body-md font-medium">System / Settings</span>
            </NavLink>
          </nav>
        </div>
      </aside>

      <main className={`flex-1 flex flex-col relative w-full pt-16 pb-20 bg-surface min-h-[calc(100vh-5rem)] ${sidebarOpen ? 'pl-72' : ''}`}>
        <div className="flex flex-col w-full px-gutter py-space-sm space-y-space-md max-w-7xl mx-auto">
          {children}
        </div>
      </main>

      <BottomNav />

      {sidebarOpen && (
        <div className="fixed inset-0 bg-black/50 z-30" onClick={() => setSidebarOpen(false)} />
      )}
    </div>
  )
}