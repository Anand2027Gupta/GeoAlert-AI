import { BrowserRouter, Routes, Route } from 'react-router-dom'
import OverviewPage from './pages/OverviewPage'
import OpenPitPage from './pages/OpenPitPage'
import UndergroundPage from './pages/UndergroundPage'
import AIAssistantPage from './pages/AIAssistantPage'
import AlertsPage from './pages/AlertsPage'
import UploadPage from './pages/UploadPage'
import ReportsPage from './pages/ReportsPage'
import HelpDeskPage from './pages/HelpDeskPage'
import SettingsPage from './pages/SettingsPage'
import Shell from './components/Shell'

function App() {
  return (
    <BrowserRouter>
      <Shell>
        <Routes>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/open-pit" element={<OpenPitPage />} />
          <Route path="/underground" element={<UndergroundPage />} />
          <Route path="/ai-assistant" element={<AIAssistantPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/help-desk" element={<HelpDeskPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Shell>
    </BrowserRouter>
  )
}

export default App
