import { useState } from 'react'

export default function SettingsPage() {
  return (
    <div className="flex flex-col w-full px-gutter py-space-sm space-y-space-md max-w-7xl mx-auto">
      <h1 className="scada-page-title">System / Settings</h1>
      <p className="scada-page-subtitle">Configure system preferences</p>
    </div>
  )
}