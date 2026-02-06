import { useState } from 'react'
import { Panel } from '@/types/panel'
import { Group } from '@/types/group'
import { CalculationResult } from '@/types/calculation'
import { FastenerDict, FastenerInclude } from '@/types/fastener'
import { ExtraPart } from '@/types/part'
import { doCalculation, calculateFasteners } from '@/services/calculationEngine'
import Layout from '@/components/layout/Layout'
import PanelSelector from '@/components/panels/PanelSelector'
import GroupsInput from '@/components/groups/GroupsInput'
import CalculateButton from '@/components/calculator/CalculateButton'
import CalculationResults from '@/components/calculator/CalculationResults'
import ChannelsSection from '@/components/calculator/ChannelsSection'
import ExtraPartsSection from '@/components/calculator/ExtraPartsSection'
import ExportSection from '@/components/export/ExportSection'
import './styles/rtl.css'

export default function App() {
  const [projectName, setProjectName] = useState('')
  const [selectedPanel, setSelectedPanel] = useState<Panel | null>(null)
  const [verticalGroups, setVerticalGroups] = useState<Group[]>([])
  const [horizontalGroups, setHorizontalGroups] = useState<Group[]>([])
  const [calcResult, setCalcResult] = useState<CalculationResult | null>(null)
  const [koshrotQty, setKoshrotQty] = useState<{ [length: string]: number }>({})
  const [manualRails, setManualRails] = useState<{ [length: string]: number }>({})
  const [fasteners, setFasteners] = useState<FastenerDict>({})
  const [fastenersInclude, setFastenersInclude] = useState<FastenerInclude>({})
  const [channelOrder, setChannelOrder] = useState<{ [name: string]: number }>({})
  const [extraParts, setExtraParts] = useState<ExtraPart[]>([])

  const handleCalculate = () => {
    if (!selectedPanel) return

    const groups = [...verticalGroups, ...horizontalGroups]
    const result = doCalculation(selectedPanel, groups)
    setCalcResult(result)

    // Initialize koshrot quantities
    const rails: { [length: string]: number } = {}
    for (const [length, qty] of Object.entries(result.autoRails)) {
      rails[String(length)] = qty
    }
    setKoshrotQty(rails)

    // Calculate fasteners
    const newFasteners = calculateFasteners(result, rails, {})
    setFasteners(newFasteners)
    setFastenersInclude(
      Object.keys(newFasteners).reduce(
        (acc, key) => {
          acc[key] = true
          return acc
        },
        {} as FastenerInclude
      )
    )
  }

  return (
    <Layout>
      <div className="space-y-6">
        {/* Project Name */}
        <section className="bg-white rounded-lg p-4 shadow-sm">
          <label className="block text-sm font-semibold mb-2">שם פרויקט</label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            className="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:border-primary-color"
            placeholder="הזן שם פרויקט"
          />
        </section>

        {/* Panel Selection */}
        <PanelSelector selectedPanel={selectedPanel} onSelectPanel={setSelectedPanel} />

        {/* Groups Input */}
        {selectedPanel && (
          <GroupsInput
            verticalGroups={verticalGroups}
            horizontalGroups={horizontalGroups}
            onVerticalChange={setVerticalGroups}
            onHorizontalChange={setHorizontalGroups}
          />
        )}

        {/* Calculate Button */}
        {selectedPanel && (
          <CalculateButton onClick={handleCalculate} />
        )}

        {/* Calculation Results */}
        {calcResult && (
          <>
            <CalculationResults
              calcResult={calcResult}
              koshrotQty={koshrotQty}
              manualRails={manualRails}
              fasteners={fasteners}
              fastenersInclude={fastenersInclude}
              onKoshrotQtyChange={setKoshrotQty}
              onManualRailsChange={setManualRails}
              onFastenersChange={setFasteners}
              onFastenersIncludeChange={setFastenersInclude}
            />

            <ChannelsSection
              channelOrder={channelOrder}
              onChannelOrderChange={setChannelOrder}
            />

            <ExtraPartsSection
              extraParts={extraParts}
              onExtraPartsChange={setExtraParts}
            />

            <ExportSection
              projectName={projectName}
              panelName={selectedPanel?.name || ''}
              calcResult={calcResult}
              koshrotQty={koshrotQty}
              manualRails={manualRails}
              fasteners={fasteners}
              fastenersInclude={fastenersInclude}
              channelOrder={channelOrder}
              extraParts={extraParts}
            />
          </>
        )}
      </div>
    </Layout>
  )
}
