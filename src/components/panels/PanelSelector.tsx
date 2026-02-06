import { Panel } from '@/types/panel'
import { useState, useEffect } from 'react'

interface PanelSelectorProps {
  selectedPanel: Panel | null
  onSelectPanel: (panel: Panel) => void
}

export default function PanelSelector({ selectedPanel, onSelectPanel }: PanelSelectorProps) {
  const [panels, setPanels] = useState<Panel[]>([])

  useEffect(() => {
    // Load panels from localStorage (demo data)
    const stored = localStorage.getItem('panels')
    if (stored) {
      setPanels(JSON.parse(stored))
    } else {
      // Default panels
      const defaultPanels: Panel[] = [
        { id: 1, name: '640W', width: 2060, height: 1030 },
        { id: 2, name: '595W', width: 2273, height: 1134 },
        { id: 3, name: '550W', width: 2232, height: 1139 },
      ]
      setPanels(defaultPanels)
      localStorage.setItem('panels', JSON.stringify(defaultPanels))
    }
  }, [])

  return (
    <section className="bg-white rounded-lg p-4 shadow-sm">
      <label className="block text-sm font-semibold mb-3">סוג פאנל</label>
      <select
        value={selectedPanel?.id || ''}
        onChange={(e) => {
          const panel = panels.find((p) => p.id === parseInt(e.target.value))
          if (panel) onSelectPanel(panel)
        }}
        className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:border-primary-color"
      >
        <option value="">בחר פאנל</option>
        {panels.map((panel) => (
          <option key={panel.id} value={panel.id}>
            {panel.name} ({panel.width}x{panel.height} cm)
          </option>
        ))}
      </select>
    </section>
  )
}
