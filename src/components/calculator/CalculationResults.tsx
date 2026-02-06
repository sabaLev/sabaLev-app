import { CalculationResult } from '@/types/calculation'
import { FastenerDict, FastenerInclude } from '@/types/fastener'
import { useState } from 'react'
import { calculateFasteners, formatLengthForDisplay, lengthSortKey } from '@/services/calculationEngine'
import './calculator.css'

interface CalculationResultsProps {
  calcResult: CalculationResult
  koshrotQty: { [length: string]: number }
  manualRails: { [length: string]: number }
  fasteners: FastenerDict
  fastenersInclude: FastenerInclude
  onKoshrotQtyChange: (qty: { [length: string]: number }) => void
  onManualRailsChange: (rails: { [length: string]: number }) => void
  onFastenersChange: (fasteners: FastenerDict) => void
  onFastenersIncludeChange: (include: FastenerInclude) => void
}

export default function CalculationResults({
  calcResult,
  koshrotQty,
  manualRails,
  fasteners,
  fastenersInclude,
  onKoshrotQtyChange,
  onManualRailsChange,
  onFastenersChange,
  onFastenersIncludeChange,
}: CalculationResultsProps) {
  const [expandedRails, setExpandedRails] = useState(true)
  const [expandedManualRails, setExpandedManualRails] = useState(false)
  const [expandedFasteners, setExpandedFasteners] = useState(true)
  const [manualRailsInput, setManualRailsInput] = useState<{ length: string; qty: string }[]>([
    { length: '', qty: '' },
  ])

  const handleKoshrotQtyChange = (length: string, value: number) => {
    const updated = { ...koshrotQty, [length]: value }
    onKoshrotQtyChange(updated)

    // Recalculate fasteners
    const newFasteners = calculateFasteners(calcResult, updated, manualRails)
    onFastenersChange(newFasteners)
  }

  const handleManualRailAdd = () => {
    const updated = { ...manualRails }
    manualRailsInput.forEach(({ length, qty }) => {
      if (length && qty) {
        updated[length] = (updated[length] || 0) + parseInt(qty)
      }
    })
    onManualRailsChange(updated)
    setManualRailsInput([{ length: '', qty: '' }])

    // Recalculate fasteners
    const newFasteners = calculateFasteners(calcResult, koshrotQty, updated)
    onFastenersChange(newFasteners)
  }

  const handleFastenerChange = (label: string, value: number) => {
    const updated = { ...fasteners, [label]: value }
    onFastenersChange(updated)
  }

  const handleFastenerIncludeChange = (label: string, included: boolean) => {
    const updated = { ...fastenersInclude, [label]: included }
    onFastenersIncludeChange(updated)
  }

  const sortedRails = Object.keys(koshrotQty).sort((a, b) => {
    const aNum = lengthSortKey(a)
    const bNum = lengthSortKey(b)
    return bNum - aNum
  })

  return (
    <div className="space-y-4">
      {/* Total Panels */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <p className="text-lg font-semibold">סה"כ פאנלים: <span className="text-primary-color">{calcResult.totalPanels}</span></p>
      </div>

      {/* Auto Rails */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <button
          onClick={() => setExpandedRails(!expandedRails)}
          className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition font-semibold"
        >
          קושרות (אוטומטי)
          <span className={`transition transform ${expandedRails ? 'rotate-180' : ''}`}>▼</span>
        </button>

        {expandedRails && (
          <div className="p-4 space-y-3">
            {sortedRails.map((length) => (
              <div key={length} className="flex gap-3">
                <label className="text-sm font-medium min-w-max">אורך: {formatLengthForDisplay(length)} ס"מ</label>
                <input
                  type="number"
                  min="0"
                  value={koshrotQty[length]}
                  onChange={(e) => handleKoshrotQtyChange(length, parseInt(e.target.value) || 0)}
                  className="flex-1 px-3 py-2 border border-neutral-300 rounded focus:outline-none focus:border-primary-color"
                />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Manual Rails */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <button
          onClick={() => setExpandedManualRails(!expandedManualRails)}
          className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition font-semibold"
        >
          קושרות (הוספה ידנית)
          <span className={`transition transform ${expandedManualRails ? 'rotate-180' : ''}`}>▼</span>
        </button>

        {expandedManualRails && (
          <div className="p-4 space-y-3">
            <div className="grid grid-cols-2 gap-2 mb-3 text-sm font-medium">
              <div>אורך (ס"מ)</div>
              <div>כמות</div>
            </div>

            {manualRailsInput.map((row, index) => (
              <div key={index} className="grid grid-cols-2 gap-2">
                <input
                  type="number"
                  min="0"
                  value={row.length}
                  onChange={(e) => {
                    const updated = [...manualRailsInput]
                    updated[index].length = e.target.value
                    setManualRailsInput(updated)
                  }}
                  placeholder="אורך"
                  className="px-3 py-2 border border-neutral-300 rounded focus:outline-none focus:border-primary-color"
                />
                <input
                  type="number"
                  min="0"
                  value={row.qty}
                  onChange={(e) => {
                    const updated = [...manualRailsInput]
                    updated[index].qty = e.target.value
                    setManualRailsInput(updated)
                  }}
                  placeholder="כמות"
                  className="px-3 py-2 border border-neutral-300 rounded focus:outline-none focus:border-primary-color"
                />
              </div>
            ))}

            <button
              onClick={() => setManualRailsInput([...manualRailsInput, { length: '', qty: '' }])}
              className="w-full py-2 text-primary-color font-medium border border-primary-light rounded hover:bg-primary-light hover:text-white transition"
            >
              הוסף שורה
            </button>

            <button
              onClick={handleManualRailAdd}
              className="w-full py-2 bg-primary-color text-white font-medium rounded hover:bg-primary-dark transition"
            >
              שמור קושרות
            </button>

            {Object.entries(manualRails).length > 0 && (
              <div className="border-t pt-3">
                <p className="text-sm font-medium mb-2">קושרות שנוספו:</p>
                {Object.entries(manualRails).map(([length, qty]) => (
                  <p key={length} className="text-sm">
                    {formatLengthForDisplay(length)} ס"מ: {qty}
                  </p>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Fasteners */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <button
          onClick={() => setExpandedFasteners(!expandedFasteners)}
          className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition font-semibold"
        >
          פרזול (אביזרים וברגים)
          <span className={`transition transform ${expandedFasteners ? 'rotate-180' : ''}`}>▼</span>
        </button>

        {expandedFasteners && (
          <div className="p-4 space-y-4">
            {Object.entries(fasteners).map(([label, value]) => (
              <div key={label} className="flex items-center gap-3">
                <input
                  type="checkbox"
                  checked={fastenersInclude[label] || false}
                  onChange={(e) => handleFastenerIncludeChange(label, e.target.checked)}
                  className="w-5 h-5 cursor-pointer"
                />
                <input
                  type="number"
                  min="0"
                  value={value}
                  onChange={(e) => handleFastenerChange(label, parseInt(e.target.value) || 0)}
                  className="w-20 px-2 py-2 border border-neutral-300 rounded text-center focus:outline-none focus:border-primary-color"
                />
                <label className="text-sm flex-1">{label}</label>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
