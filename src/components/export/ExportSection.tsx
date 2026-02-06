import { CalculationResult } from '@/types/calculation'
import { FastenerDict, FastenerInclude } from '@/types/fastener'
import { ExtraPart } from '@/types/part'
import { useState } from 'react'
import { formatLengthForDisplay } from '@/services/calculationEngine'

interface ExportSectionProps {
  projectName: string
  panelName: string
  calcResult: CalculationResult
  koshrotQty: { [length: string]: number }
  manualRails: { [length: string]: number }
  fasteners: FastenerDict
  fastenersInclude: FastenerInclude
  channelOrder: { [name: string]: number }
  extraParts: ExtraPart[]
}

export default function ExportSection({
  projectName,
  panelName,
  koshrotQty,
  manualRails,
  fasteners,
  fastenersInclude,
  channelOrder,
  extraParts,
}: ExportSectionProps) {
  const [expanded, setExpanded] = useState(false)
  const [showPreview, setShowPreview] = useState(false)

  const generateHtmlReport = () => {
    const railsTotal: { [key: string]: number } = {}

    // Add auto rails
    for (const [length, qty] of Object.entries(koshrotQty)) {
      const display = formatLengthForDisplay(length)
      railsTotal[display] = (railsTotal[display] || 0) + qty
    }

    // Add manual rails
    for (const [length, qty] of Object.entries(manualRails)) {
      const display = formatLengthForDisplay(length)
      railsTotal[display] = (railsTotal[display] || 0) + qty
    }

    let html = `
      <!DOCTYPE html>
      <html dir="rtl" lang="he">
      <head>
        <meta charset="UTF-8">
        <title>דו"ח מערכת סולארית</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            direction: rtl;
            text-align: right;
            margin: 30px;
            line-height: 1.6;
            color: #333;
          }
          h1 { font-size: 24px; margin-bottom: 20px; }
          h2 { font-size: 18px; margin-top: 24px; margin-bottom: 12px; border-bottom: 2px solid #2563eb; padding-bottom: 8px; }
          table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
          td { padding: 8px; border-bottom: 1px solid #ddd; }
          .total { font-weight: bold; }
          .number { text-align: left; font-weight: bold; }
        </style>
      </head>
      <body>
        <h1>${projectName || 'דו"ח מערכת סולארית'}</h1>
        <p><strong>סוג פאנל:</strong> ${panelName}</p>
        <p><strong>תאריך:</strong> ${new Date().toLocaleDateString('he-IL')}</p>
    `

    // Rails section
    html += '<h2>קושרות (כמות × אורך)</h2>'
    html += '<table>'
    const sortedRails = Object.entries(railsTotal).sort(
      (a, b) => parseFloat(b[0]) - parseFloat(a[0])
    )
    for (const [length, qty] of sortedRails) {
      html += `<tr><td>${length} ס"מ</td><td class="number">${qty}</td></tr>`
    }
    html += '</table>'

    // Fasteners section
    const visibleFasteners = Object.entries(fasteners).filter(
      ([label]) => fastenersInclude[label] && fasteners[label] > 0
    )

    if (visibleFasteners.length > 0) {
      html += '<h2>פרזול</h2>'
      html += '<table>'
      for (const [label, qty] of visibleFasteners) {
        html += `<tr><td>${label}</td><td class="number">${qty}</td></tr>`
      }
      html += '</table>'
    }

    // Channels section
    if (Object.keys(channelOrder).length > 0) {
      html += '<h2>תעלות עם מכסים (מטר)</h2>'
      html += '<table>'
      for (const [name, qty] of Object.entries(channelOrder)) {
        html += `<tr><td>${name}</td><td class="number">${qty}</td></tr>`
      }
      html += '</table>'
    }

    // Extra parts section
    if (extraParts.length > 0) {
      html += '<h2>פריטים נוספים</h2>'
      html += '<table>'
      for (const part of extraParts) {
        html += `<tr><td>${part.name}</td><td class="number">${part.qty}</td></tr>`
      }
      html += '</table>'
    }

    html += `
      </body>
      </html>
    `

    return html
  }

  const handleExport = () => {
    const html = generateHtmlReport()
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `solar-report-${projectName || 'export'}.html`
    link.click()
  }

  const handlePrint = () => {
    const html = generateHtmlReport()
    const printWindow = window.open('', '', 'height=600,width=800')
    if (printWindow) {
      printWindow.document.write(html)
      printWindow.document.close()
      setTimeout(() => printWindow.print(), 250)
    }
  }

  const htmlReport = generateHtmlReport()

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full px-4 py-3 flex justify-between items-center bg-neutral-50 hover:bg-neutral-100 border-b border-neutral-200 transition font-semibold"
      >
        ייצוא דו"ח
        <span className={`transition transform ${expanded ? 'rotate-180' : ''}`}>▼</span>
      </button>

      {expanded && (
        <div className="p-4 space-y-3">
          <button
            onClick={handleExport}
            className="w-full py-2 bg-info-color hover:bg-info-light text-white font-medium rounded transition"
          >
            ייצוא כ-HTML
          </button>

          <button
            onClick={handlePrint}
            className="w-full py-2 bg-neutral-600 hover:bg-neutral-700 text-white font-medium rounded transition"
          >
            הדפס
          </button>

          <button
            onClick={() => setShowPreview(!showPreview)}
            className="w-full py-2 bg-primary-light hover:bg-primary-color text-white font-medium rounded transition"
          >
            {showPreview ? 'הסתר תצוגה מקדימה' : 'הצג תצוגה מקדימה'}
          </button>

          {showPreview && (
            <div className="border border-neutral-200 rounded p-4 bg-neutral-50 max-h-96 overflow-y-auto">
              <iframe
                srcDoc={htmlReport}
                className="w-full h-96 border-0 rounded"
                title="Report Preview"
              />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
