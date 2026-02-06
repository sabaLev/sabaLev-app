import { Group } from '@/types/group'
import { useState } from 'react'
import './groups.css'

interface GroupsInputProps {
  verticalGroups: Group[]
  horizontalGroups: Group[]
  onVerticalChange: (groups: Group[]) => void
  onHorizontalChange: (groups: Group[]) => void
}

export default function GroupsInput({
  verticalGroups,
  horizontalGroups,
  onVerticalChange,
  onHorizontalChange,
}: GroupsInputProps) {
  const [expandedVertical, setExpandedVertical] = useState(true)
  const [expandedHorizontal, setExpandedHorizontal] = useState(true)

  const handleVerticalChange = (index: number, field: 'panelsCount' | 'groupsCount', value: number) => {
    const updated = [...verticalGroups]
    updated[index] = { ...updated[index], [field]: value }
    onVerticalChange(updated)
  }

  const handleHorizontalChange = (index: number, field: 'panelsCount' | 'groupsCount', value: number) => {
    const updated = [...horizontalGroups]
    updated[index] = { ...updated[index], [field]: value }
    onHorizontalChange(updated)
  }

  const addVerticalRow = () => {
    onVerticalChange([...verticalGroups, { panelsCount: 0, groupsCount: 0, orientation: 'עומד' }])
  }

  const addHorizontalRow = () => {
    onHorizontalChange([...horizontalGroups, { panelsCount: 0, groupsCount: 0, orientation: 'שוכב' }])
  }

  return (
    <div className="space-y-4">
      {/* Vertical Groups */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <button
          onClick={() => setExpandedVertical(!expandedVertical)}
          className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition"
        >
          <span className="font-semibold">עומדים (פאנלים בעמידה)</span>
          <span className={`transition transform ${expandedVertical ? 'rotate-180' : ''}`}>▼</span>
        </button>

        {expandedVertical && (
          <div className="p-4 space-y-3">
            <div className="grid grid-cols-3 gap-2 mb-3 text-sm font-medium">
              <div></div>
              <div className="text-center">פאנלים בשורה</div>
              <div className="text-center">מספר שורות</div>
            </div>

            {verticalGroups.map((group, index) => (
              <div key={index} className="grid grid-cols-3 gap-2">
                <div className="flex items-center text-sm">{index + 1}</div>
                <input
                  type="number"
                  min="0"
                  max="50"
                  value={group.panelsCount}
                  onChange={(e) => handleVerticalChange(index, 'panelsCount', parseInt(e.target.value) || 0)}
                  className="px-2 py-2 border border-neutral-300 rounded text-center focus:outline-none focus:border-primary-color"
                />
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={group.groupsCount}
                  onChange={(e) => handleVerticalChange(index, 'groupsCount', parseInt(e.target.value) || 0)}
                  className="px-2 py-2 border border-neutral-300 rounded text-center focus:outline-none focus:border-primary-color"
                />
              </div>
            ))}

            <button
              onClick={addVerticalRow}
              className="w-full py-2 mt-3 bg-primary-light text-white rounded-lg hover:bg-primary-color transition font-medium text-sm"
            >
              הוסף שורה
            </button>
          </div>
        )}
      </div>

      {/* Horizontal Groups */}
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <button
          onClick={() => setExpandedHorizontal(!expandedHorizontal)}
          className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition"
        >
          <span className="font-semibold">שוכבים (פאנלים ממוזגים)</span>
          <span className={`transition transform ${expandedHorizontal ? 'rotate-180' : ''}`}>▼</span>
        </button>

        {expandedHorizontal && (
          <div className="p-4 space-y-3">
            <div className="grid grid-cols-3 gap-2 mb-3 text-sm font-medium">
              <div></div>
              <div className="text-center">פאנלים בשורה</div>
              <div className="text-center">מספר שורות</div>
            </div>

            {horizontalGroups.map((group, index) => (
              <div key={index} className="grid grid-cols-3 gap-2">
                <div className="flex items-center text-sm">{index + 1}</div>
                <input
                  type="number"
                  min="0"
                  max="50"
                  value={group.panelsCount}
                  onChange={(e) => handleHorizontalChange(index, 'panelsCount', parseInt(e.target.value) || 0)}
                  className="px-2 py-2 border border-neutral-300 rounded text-center focus:outline-none focus:border-primary-color"
                />
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={group.groupsCount}
                  onChange={(e) => handleHorizontalChange(index, 'groupsCount', parseInt(e.target.value) || 0)}
                  className="px-2 py-2 border border-neutral-300 rounded text-center focus:outline-none focus:border-primary-color"
                />
              </div>
            ))}

            <button
              onClick={addHorizontalRow}
              className="w-full py-2 mt-3 bg-primary-light text-white rounded-lg hover:bg-primary-color transition font-medium text-sm"
            >
              הוסף שורה
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
