import { useState } from 'react'

const MICRO_SEISMIC_EVENTS = [
  { id: 1, magnitude: 'ML 1.2', type: 'Crown Pillar Shear', coord: '420L / 12W / XC4.2', time: '14:18:02', relative: '12 mins ago', severity: 'critical' },
  { id: 2, magnitude: 'ML 0.8', type: 'Hanging Wall Spall', coord: '420L / 12W / XC3.8', time: '13:42:55', relative: '48 mins ago', severity: 'warning' },
  { id: 3, magnitude: 'ML 0.4', type: 'Stress Redistribution', coord: '420L / Footwall Ramp', time: '12:11:18', relative: '2h 19m ago', severity: 'nominal' },
]

export default function UndergroundPage() {
  const [isRunning, setIsRunning] = useState(false)

  const runPrediction = () => {
    setIsRunning(true)
    setTimeout(() => setIsRunning(false), 800)
  }

  return (
    <div className="flex flex-col w-full px-gutter py-space-sm space-y-space-md max-w-7xl mx-auto">
      <header className="fixed top-0 w-full z-50 pt-safe bg-surface/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.4)]">
        <div className="h-16 px-gutter flex items-center justify-between gap-space-sm">
          <div className="flex items-center gap-space-sm">
            <button
              className="w-11 h-11 flex items-center justify-center rounded text-on-surface hover:text-primary active:bg-surface-container"
              type="button"
            >
              <span className="material-symbols-outlined text-[24px]">arrow_back</span>
            </button>
            <img
              alt="GeoAlert AI Logo"
              className="h-8 w-auto object-contain"
              src="https://lh3.googleusercontent.com/aida/AEtjO1VmrHHBtuimom0dJKmKl0QNf7IZY0Knjw47so3IWM7SZd8E1uBjGrcXvPPGA49tTGYxb1aS9fwnrvyR5-VesOalT-YjBDresAZSUwM8BNFkFXsEgjUThzBtbDPOPXo-NFznd1DecI3goSoNEQhdMy451wjeVE8rW3tTZ3s0Xe-Kc2r-rrbrPP5uPvWvZqMRb3IbssygU88rIlypz1aTsO65WdtNQNL2Q4z71DISXAJvpLF-u8vljswP"
            />
            <div className="flex flex-col">
              <h1 className="scada-page-title tracking-tight uppercase">Underground Monitoring</h1>
              <span className="font-label-sm text-label-sm text-secondary uppercase tracking-wider">GEOALERT AI • NB-4B</span>
            </div>
          </div>
          <div className="flex items-center gap-space-xs">
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
              <span className="text-on-primary text-[18px]">person</span>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-1 flex flex-col relative w-full pt-16 pb-safe bg-surface min-h-screen">
        <div className="flex flex-col w-full p-gutter gap-space-md">
          <div className="flex flex-col gap-space-xs bg-surface-container-low p-space-md rounded-xl shadow-md">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-space-xs">
                <span className="w-2 h-2 rounded-full bg-error animate-ping" />
                <span className="font-label-sm text-label-sm uppercase text-secondary tracking-widest">Subsurface Sensor Network</span>
              </div>
              <span className="font-label-sm text-label-sm bg-surface-container-highest px-2 py-0.5 rounded text-on-surface-variant">SCADA v4.8</span>
            </div>
            <div className="flex flex-col">
              <h2 className="font-headline-md text-headline-md text-on-surface tracking-tight">Underground Stope & Drift Monitoring</h2>
              <p className="scada-page-subtitle">Tunnel Roof Fall Risk, Pillar Stress & Micro-Seismic Activity</p>
            </div>
            <div className="mt-space-xs bg-surface-container p-space-xs rounded-lg flex items-center justify-between">
              <div className="flex items-center gap-space-xs min-w-0">
                <div className="w-7 h-7 rounded bg-surface-container-high flex items-center justify-center shrink-0">
                  <span className="material-symbols-outlined text-secondary text-[16px]">layers</span>
                </div>
                <div className="flex flex-col min-w-0">
                  <span className="font-label-sm text-label-sm text-on-surface-variant leading-none">CURRENT VECTOR</span>
                  <span className="font-body-md text-body-md text-on-surface font-mono font-bold">+12.4 mm/h • dX trending up</span>
                </div>
              </div>
              <span className="font-label-sm text-label-sm text-secondary">SYNCED</span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-space-md">
            <div className="lg:col-span-2">
              <div className="scada-card-elevated">
                <h3 className="font-label-md text-label-md text-on-surface mb-space-md">Micro-Seismic Historical Trend Log</h3>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-space-xs">
                    <span className="material-symbols-outlined text-secondary text-[18px]">history</span>
                    <span className="font-label-sm text-label-sm uppercase font-bold text-on-surface tracking-wider">Shift Micro-Seismic Sequence</span>
                  </div>
                  <span className="font-label-sm text-label-sm text-on-surface-variant font-mono">LAST 6 HOURS</span>
                </div>
                <div className="mt-space-sm space-y-0">
                  {MICRO_SEISMIC_EVENTS.map((event) => (
                    <div key={event.id} className="bg-surface-container-high p-space-xs rounded flex items-center justify-between">
                      <div className="flex items-center gap-space-xs">
                        <span className={`w-2 h-2 rounded-full shrink-0 ${event.severity === 'critical' ? 'bg-[#EF4444]' : event.severity === 'warning' ? 'bg-[#ffb690]' : 'bg-[#7bd0ff]'}`} />
                        <div className="flex flex-col">
                          <span className="font-label-sm text-label-sm text-on-surface font-mono font-semibold">{event.magnitude} • {event.type}</span>
                          <span className="font-body-sm text-[10px] text-on-surface-variant">{event.coord}</span>
                        </div>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className={`font-label-sm text-label-sm text-on-surface font-mono font-bold ${event.severity === 'critical' ? 'text-[#EF4444]' : event.severity === 'warning' ? 'text-[#ffb690]' : 'text-[#7bd0ff]'}`}>
                          {event.time}
                        </span>
                        <span className="font-label-sm text-[9px] text-on-surface-variant">{event.relative}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="lg:col-span-1">
              <div className="scada-card-elevated">
                <h3 className="font-label-md text-label-md text-on-surface mb-space-sm">Underground Prediction</h3>
                <div className="flex items-center justify-center p-space-md">
                  <button
                    className="scada-btn-primary w-full"
                    onClick={runPrediction}
                    disabled={isRunning}
                  >
                    {isRunning ? (
                      <>
                        <span className="material-symbols-outlined text-[20px] animate-spin">refresh</span>
                        <span>Computing...</span>
                      </>
                    ) : (
                      <>
                        <span className="material-symbols-outlined text-[20px]">smart_toy</span>
                        <span>Run Prediction</span>
                      </>
                    )}
                  </button>
                </div>
                <p className="font-body-sm text-[11px] text-on-surface-variant text-center mt-space-xs">
                  Demo simulation — not connected to live ML model.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}