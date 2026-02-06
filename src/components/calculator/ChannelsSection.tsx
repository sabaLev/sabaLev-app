import { useState } from 'react'

interface ChannelsSectionProps {
  channelOrder: { [name: string]: number }
  onChannelOrderChange: (order: { [name: string]: number }) => void
}

const DEFAULT_CHANNELS = [
  { name: 'ערוץ C (רשת)', step: 3.0 },
  { name: 'ערוץ C (פח)', step: 2.5 },
  { name: 'ערוץ Z (רשת)', step: 3.0 },
  { name: 'ערוץ Z (פח)', step: 2.5 },
]

export default function ChannelsSection({
  channelOrder,
  onChannelOrderChange,
}: ChannelsSectionProps) {
  const [expanded, setExpanded] = useState(true)

  const handleChannelChange = (name: string, value: number) => {
    const updated = { ...channelOrder, [name]: value }
    // Remove zero values
    if (value === 0) {
      delete updated[name]
    }
    onChannelOrderChange(updated)
  }

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition font-semibold"
      >
        תעלות עם מכסים (מטר)
        <span className={`transition transform ${expanded ? 'rotate-180' : ''}`}>▼</span>
      </button>

      {expanded && (
        <div className="p-4 space-y-3">
          {DEFAULT_CHANNELS.map((channel) => (
            <div key={channel.name} className="flex gap-3">
              <label className="text-sm font-medium min-w-max">{channel.name}</label>
              <input
                type="number"
                min="0"
                step={channel.step}
                value={channelOrder[channel.name] || 0}
                onChange={(e) => handleChannelChange(channel.name, parseFloat(e.target.value) || 0)}
                className="flex-1 px-3 py-2 border border-neutral-300 rounded focus:outline-none focus:border-primary-color"
              />
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
