
import { useState } from 'react'

const SECTORS = [
  'Sector 4 — North Bench Wall (Highwall C)',
  'Sector 2 — South Bench Wall',
  'Sector 7 — East Pit Crest',
  'Sector 1 — West Access Ramp',
]

const PARAMS = [
  { label: 'Bench Angle', id: 'bench-angle', unit: '°', default: 68, min: 45, max: 80 },
  { label: 'Slope Height', id: 'slope-height', unit: 'm', default: 45, min: 20, max: 120 },
  { label: 'Pit Slope', id: 'pit-slope', unit: '°', default: 42, min: 30, max: 60 },
  { label: 'RMR Rating', id: 'rmr-rating', unit: '', default: 48, min: 20, max: 90 },
  { label: 'GSI Index', id: 'gsi-index', unit: '', default: 52, min: 20, max: 90 },
  { label: 'Joint Spacing', id: 'joint-spacing', unit: 'm', default: 0.35, min: 0.1, max: 2.0, step: 0.05 },
  { label: 'GW Depth', id: 'gw-depth', unit: ' m', default: 18, min: 5, max: 50 },
  { label: 'Precip 24h', id: 'precip-24h', unit: 'mm', default: 28.4, min: 0, max: 100 },
  { label: 'Blast PPV', id: 'blast-ppv', unit: 'mm/s', default: 14.2, min: 0, max: 50 },
]

export default function OpenPitPage() {
  const [selectedSector, setSelectedSector] = useState(SECTORS[0])
  const [showDropdown, setShowDropdown] = useState(false)

  const [params, setParams] = useState(
    Object.fromEntries(PARAMS.map(p => [p.id, p.default]))
  )

  // Inputs supported by the current backend model
  const [fs, setFs] = useState(1.5)
  const [reinforcement, setReinforcement] = useState(2.0)

  const [inferenceResult, setInferenceResult] = useState(null)
  const [isComputing, setIsComputing] = useState(false)

  const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

  const fetchPrediction = async (fsValue, reinforcementValue) => {
    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          mine_type: 'open-pit',
          open_pit: {
            fs: fsValue,
            reinforcement: reinforcementValue,
          },
        }),
      })

      if (!response.ok) {
        let errorMessage = `Server error: ${response.status}`

        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
        } catch {
          // Keep the HTTP status message if the response is not JSON
        }

        throw new Error(errorMessage)
      }

      const data = await response.json()
      return { success: true, data }
    } catch (error) {
      return {
        success: false,
        error: error.message || 'Network error',
      }
    }
  }

  const runInference = async () => {
    setIsComputing(true)
    setInferenceResult(null)

    try {
      const result = await fetchPrediction(fs, reinforcement)

      if (!result.success) {
        throw new Error(result.error || 'Prediction failed')
      }

      setInferenceResult({
        fs,
        reinforcement,
        risk: result.data.risk_level,
        riskLevel: result.data.risk_level,
        riskMessage: result.data.message,
      })
    } catch (error) {
      setInferenceResult({
        fs,
        reinforcement,
        risk: 'Error',
        riskLevel: 'Error',
        riskMessage: error.message || 'Prediction failed',
      })
    } finally {
      setIsComputing(false)
    }
  }

  const riskTextClass =
    inferenceResult?.riskLevel === 'High'
      ? 'text-[#F59E0B]'
      : inferenceResult?.riskLevel === 'Low'
        ? 'text-[#22C55E]'
        : 'text-[#EF4444]'

  return (
    <div className="flex flex-col w-full px-gutter py-space-sm space-y-space-md max-w-7xl mx-auto">

      {/* Page Header */}
      <div className="flex flex-col gap-space-xs bg-surface-container-low p-space-md rounded-lg shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-space-sm">
          <div className="flex items-center gap-space-sm">
            <span className="p-1.5 rounded bg-primary-container/20 text-primary-container flex items-center justify-center">
              <span className="material-symbols-outlined text-[20px]">landscape</span>
            </span>
            <div>
              <h1 className="scada-page-title">Open-Pit Geotechnical Monitoring</h1>
              <p className="scada-page-subtitle">
                Bench Slope Stability, InSAR Radar & Pit Crest Dynamics
              </p>
            </div>
          </div>

          {/* Sector Selector */}
          <div className="relative">
            <button
              className="flex items-center gap-2 px-space-md py-1.5 rounded bg-surface-container-high hover:bg-surface-container-highest text-on-surface transition-colors"
              onClick={() => setShowDropdown(!showDropdown)}
            >
              <span className="w-2 h-2 rounded-full bg-primary-container animate-pulse" />
              <span className="font-label-md text-label-md tracking-wide uppercase">
                {selectedSector}
              </span>
              <span className="material-symbols-outlined text-[16px] text-secondary">
                expand_more
              </span>
            </button>

            {showDropdown && (
              <div className="absolute right-0 mt-1 w-72 bg-surface-container-highest shadow-xl rounded-lg z-30 p-1 space-y-0.5">
                <div className="px-space-sm py-1 font-label-sm text-label-sm text-on-surface-variant uppercase">
                  Select Open-Pit Zone
                </div>

                {SECTORS.map(s => (
                  <button
                    key={s}
                    onClick={() => {
                      setSelectedSector(s)
                      setShowDropdown(false)
                    }}
                    className="w-full text-left px-space-sm py-1.5 rounded bg-surface-container text-primary font-label-md text-label-md flex items-center justify-between"
                  >
                    {s}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Main Dashboard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-space-md">

        <div className="lg:col-span-2">
          <div className="scada-card-elevated">

            <h3 className="font-label-md text-label-md text-on-surface mb-space-md">
              Geotechnical Inference Parameters
            </h3>

            {/* Existing Geotechnical Parameters */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-space-sm">
              {PARAMS.map(p => (
                <div key={p.id} className="flex flex-col gap-space-xs">
                  <label className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                    {p.label}
                  </label>

                  <div className="flex items-end gap-space-xs">
                    <input
                      type="range"
                      min={p.min}
                      max={p.max}
                      step={p.step || 1}
                      value={params[p.id]}
                      onChange={e =>
                        setParams({
                          ...params,
                          [p.id]: Number(e.target.value),
                        })
                      }
                      className="w-full h-1 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-primary"
                    />

                    <span className={`font-label-md text-label-md font-mono ${params[p.id] > 70 ? 'text-[#EF4444]' : 'text-on-surface'}`}>
                      {params[p.id]}{p.unit}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {/* Actual Model Inputs */}
            <div className="mt-space-md border-t border-outline/30 pt-space-md">
              <h3 className="font-label-md text-label-md text-primary mb-space-sm">
                ML Model Input Parameters
              </h3>

              <p className="text-[11px] text-on-surface-variant mb-space-md">
                These two parameters are currently used by the connected open-pit prediction model.
                The nine geotechnical sliders above are not yet connected to this model.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-space-md">

                <div className="flex flex-col gap-space-xs">
                  <label className="font-label-sm text-label-sm text-on-surface-variant">
                    Factor of Safety (FS): {Number(fs).toFixed(1)}
                  </label>

                  <input
                    type="range"
                    min="1.0"
                    max="3.0"
                    step="0.1"
                    value={fs}
                    onChange={e => setFs(Number(e.target.value))}
                    className="w-full accent-primary"
                  />

                  <span className="text-[10px] text-on-surface-variant">
                    Allowed range: 1.0 – 3.0
                  </span>
                </div>

                <div className="flex flex-col gap-space-xs">
                  <label className="font-label-sm text-label-sm text-on-surface-variant">
                    Reinforcement: {Number(reinforcement).toFixed(1)}
                  </label>

                  <input
                    type="range"
                    min="0.0"
                    max="5.0"
                    step="0.1"
                    value={reinforcement}
                    onChange={e => setReinforcement(Number(e.target.value))}
                    className="w-full accent-primary"
                  />

                  <span className="text-[10px] text-on-surface-variant">
                    Allowed range: 0.0 – 5.0
                  </span>
                </div>

              </div>
            </div>

            {/* Inference Button */}
            <div className="mt-space-md">
              <button
                className="scada-btn-primary w-full"
                onClick={runInference}
                disabled={isComputing}
              >
                {isComputing ? (
                  <>
                    <span className="material-symbols-outlined text-[20px] animate-spin">
                      sync
                    </span>
                    <span>Running inference...</span>
                  </>
                ) : (
                  <>
                    <span className="material-symbols-outlined text-[20px]">
                      smart_toy
                    </span>
                    <span>Run Open-Pit Hazard Inference</span>
                  </>
                )}
              </button>
            </div>

            {/* Single Prediction Result Panel */}
            {inferenceResult && (
              <div className="mt-space-md p-space-md rounded bg-surface-container-high border border-primary/30">
                <h4 className="font-label-md text-label-md text-primary mb-space-sm">
                  Inference Result
                </h4>

                <div className="grid grid-cols-2 gap-space-sm">
                  <div>
                    <span className="font-label-sm text-label-sm text-on-surface-variant">
                      Factor of Safety
                    </span>
                    <p className="font-body-md text-body-md text-on-surface">
                      {inferenceResult.fs}
                    </p>
                  </div>

                  <div>
                    <span className="font-label-sm text-label-sm text-on-surface-variant">
                      Reinforcement
                    </span>
                    <p className="font-body-md text-body-md text-on-surface">
                      {inferenceResult.reinforcement}
                    </p>
                  </div>
                </div>

                <p className="mt-space-sm font-label-sm text-label-sm text-on-surface-variant">
                  Risk Level:{' '}
                  <span className={`${riskTextClass} font-bold`}>
                    {inferenceResult.risk}
                  </span>
                </p>

                <p className="font-body-sm text-[11px] text-on-surface-variant mt-space-xs">
                  {inferenceResult.riskMessage}
                </p>

                <p className="font-body-sm text-[11px] text-on-surface-variant mt-space-xs">
                  Prediction is generated by the connected local backend model.
                  It is not a substitute for a professional mine-safety assessment.
                </p>
              </div>
            )}

          </div>
        </div>

        {/* Right Sidebar */}
        <div className="lg:col-span-1">

          {/* Active Alerts */}
          <div className="scada-card-elevated mb-space-md">
            <h3 className="font-label-md text-label-md text-on-surface mb-space-sm">
              Active Alerts
            </h3>

            <div className="space-y-space-xs">
              {[
                { type: 'Critical', msg: 'Slope displacement rate increased 12%', time: '14:18' },
                { type: 'Warning', msg: 'InSAR coherence loss detected', time: '13:42' },
                { type: 'Info', msg: 'Radar calibration complete', time: '12:11' },
              ].map((a, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between p-space-xs rounded bg-surface-container-high border border-outline/50"
                >
                  <span className={`font-label-sm text-label-sm font-mono ${a.type === 'Critical' ? 'text-[#EF4444]' : a.type === 'Warning' ? 'text-[#F59E0B]' : 'text-[#7bd0ff]'}`}>
                    {a.type}
                  </span>

                  <div className="flex flex-col items-end">
                    <span className="font-body-sm text-[11px] text-on-surface">
                      {a.msg}
                    </span>
                    <span className="font-label-sm text-[9px] text-on-surface-variant">
                      {a.time}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Dispatch Alert */}
          <div className="scada-card">
            <h3 className="font-label-md text-label-md text-on-surface mb-space-sm">
              Dispatch Alert
            </h3>

            <button
              className="scada-btn-error w-full mt-space-sm"
              onClick={() => alert('Dispatch alert sent (demo mode)')}
            >
              <span className="material-symbols-outlined text-[14px]">
                send
              </span>
              <span>Transmit Dispatch</span>
            </button>
          </div>

          {/* Telemetry Vector */}
          <div className="scada-card mt-space-md">
            <h3 className="font-label-md text-label-md text-on-surface mb-space-sm">
              Telemetry Vector
            </h3>

            <div className="space-y-space-xs">
              {['dX', 'dY', 'dZ', 'Velocity'].map((v, i) => (
                <div
                  key={v}
                  className="flex items-center justify-between p-space-xs rounded bg-surface-container-high"
                >
                  <span className="font-label-sm text-label-sm text-on-surface-variant">
                    {v}
                  </span>

                  <span className={`font-label-md text-label-md font-mono ${i === 0 ? 'text-[#EF4444]' : 'text-on-surface'}`}>
                    {i === 0 ? '+12.4 mm/h' : i === 1 ? '-3.2 mm/h' : i === 2 ? '+0.8 mm/h' : '4.2 mm/h'}
                  </span>

                  <span className={`material-symbols-outlined text-[14px] ${i === 0 ? 'text-[#EF4444]' : 'text-[#22C55E]'}`}>
                    {i === 0 ? 'trending_up' : i === 1 ? 'trending_down' : 'trending_up'}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
