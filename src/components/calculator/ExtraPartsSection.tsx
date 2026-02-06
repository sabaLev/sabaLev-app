import { ExtraPart } from '@/types/part'
import { useState } from 'react'

interface ExtraPartsSectionProps {
  extraParts: ExtraPart[]
  onExtraPartsChange: (parts: ExtraPart[]) => void
}

const DEFAULT_PARTS = [
  { name: 'מחבר DC סימטרי 5.5-2.1', unit: 'יח׳' },
  { name: 'כבל DC סרט 2x6 ממ"ר', unit: 'מטר' },
  { name: 'מערכת עמוד', unit: 'יח׳' },
  { name: 'תא קיבול ומגן', unit: 'יח׳' },
]

export default function ExtraPartsSection({
  extraParts,
  onExtraPartsChange,
}: ExtraPartsSectionProps) {
  const [expanded, setExpanded] = useState(false)
  const [parts, setParts] = useState<(ExtraPart & { unit: string })[]>(
    DEFAULT_PARTS.map((p) => ({
      ...p,
      qty: extraParts.find((ep) => ep.name === p.name)?.qty || 0,
    }))
  )

  const handlePartChange = (index: number, qty: number) => {
    const updated = [...parts]
    updated[index] = { ...updated[index], qty }
    setParts(updated)

    const filtered = updated.filter((p) => p.qty > 0)
    onExtraPartsChange(filtered.map(({ name, qty }) => ({ name, qty })))
  }

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition font-semibold"
      >
        הוסף פריט (דיוני נוספים)
        <span className={`transition transform ${expanded ? 'rotate-180' : ''}`}>▼</span>
      </button>

      {expanded && (
        <div className="p-4 space-y-3">
          {parts.map((part, index) => (
            <div key={part.name} className="flex gap-3">
              <label className="text-sm font-medium min-w-max">{part.name}</label>
              <input
                type="number"
                min="0"
                value={part.qty || 0}
                onChange={(e) => handlePartChange(index, parseInt(e.target.value) || 0)}
                className="w-24 px-3 py-2 border border-neutral-300 rounded text-center focus:outline-none focus:border-primary-color"
              />
              <span className="text-sm text-neutral-600 min-w-max">{part.unit}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
