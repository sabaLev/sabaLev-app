import { Panel } from '@/types/panel';
import { Group, GroupOrientation } from '@/types/group';
import { CalculationResult, CalcGroupResult } from '@/types/calculation';
import { FastenerDict } from '@/types/fastener';

export function roundUpToTens(x: number): number {
  if (x <= 0) return 0;
  return Math.ceil(x / 10.0) * 10;
}

export function normalizeLengthKey(length: number | string): string {
  if (!length) return '';
  const s = String(length).trim().replace(',', '.');
  if (s === '') return '';
  try {
    const f = parseFloat(s);
    return Number.isInteger(f) ? String(Math.floor(f)) : String(f);
  } catch {
    return s;
  }
}

export function lengthSortKey(lengthKey: string): number {
  try {
    return parseFloat(String(lengthKey).replace(',', '.'));
  } catch {
    return -1.0;
  }
}

export function formatQty(q: number | string): string {
  try {
    const qf = parseFloat(String(q));
    if (Number.isInteger(qf)) {
      return String(Math.floor(qf));
    }
    const s = String(qf).replace(/0+$/, '').replace(/\.$/, '');
    return s;
  } catch {
    return String(q);
  }
}

export function formatLengthForDisplay(length: number | string): string {
  try {
    const f = parseFloat(String(length));
    if (Number.isInteger(f)) {
      return String(Math.floor(f));
    }
    const s = String(f);
    if (s.endsWith('.0')) {
      return s.slice(0, -2);
    }
    return s;
  } catch {
    return String(length);
  }
}

export function splitIntoSegments(totalLength: number): number[] {
  if (totalLength <= 0) return [];
  if (totalLength <= 550) return [totalLength];

  const full = Math.floor(totalLength / 550);
  const remainder = totalLength % 550;

  if (full === 1 && remainder > 0 && remainder < 100) {
    const half = totalLength / 2.0;
    const a = Math.round(half);
    const b = totalLength - a;
    return [a, b];
  }

  const segs: number[] = [];
  let r = totalLength;
  while (r > 550) {
    segs.push(550);
    r -= 550;
  }
  segs.push(r);
  return segs;
}

export function calcFixings(N: number): [number, number] {
  if (N === 1) return [0, 0];

  const pairs = Math.floor(N / 2);
  let earthing = pairs;
  let middle = pairs;

  if (pairs > 1) {
    middle += (pairs - 1) * 2;
  }

  if (N % 2 === 1) {
    earthing += 1;
    middle += 1;
  }

  return [earthing, middle];
}

export function calcGroup(
  N: number,
  orientation: GroupOrientation,
  panelRow: Panel
): CalcGroupResult {
  const nameStr = String(panelRow.name);

  if (nameStr.includes('640') && orientation === 'שוכב' && (N === 1 || N === 2)) {
    const final = N === 1 ? 250 : 490;
    const segs = [final];
    const connectors = 0;
    const [earthing, middle] = calcFixings(N);
    return {
      segments: segs,
      connectors,
      earthing,
      middle,
      edge: 4,
      railsPerRow: 2,
    };
  }

  const base = orientation === 'עומד' ? panelRow.width * N : panelRow.height * N;
  const fixings = N + 1;
  const raw = base + fixings * 2;
  const final = Math.ceil((raw + 10) / 10) * 10;

  const segs = splitIntoSegments(final);
  const connectors = (segs.length - 1) * 2;
  const [earthing, middle] = calcFixings(N);

  return {
    segments: segs,
    connectors,
    earthing,
    middle,
    edge: 4,
    railsPerRow: 2,
  };
}

export function doCalculation(panel: Panel, groups: Group[]): CalculationResult {
  const autoRails: { [length: number]: number } = {};
  let conn = 0,
    ear = 0,
    mid = 0,
    edge = 0;
  let totalPanels = 0;

  for (const group of groups) {
    totalPanels += group.panelsCount * group.groupsCount;

    for (let i = 0; i < group.groupsCount; i++) {
      const result = calcGroup(group.panelsCount, group.orientation, panel);

      for (const seg of result.segments) {
        autoRails[seg] = (autoRails[seg] || 0) + result.railsPerRow;
      }

      conn += result.connectors;
      ear += result.earthing;
      mid += result.middle;
      edge += result.edge;
    }
  }

  return {
    autoRails,
    connectors: conn,
    earthing: ear,
    middle: mid,
    edge,
    totalPanels,
  };
}

export function calculateFasteners(
  calcResult: CalculationResult,
  koshrotQty: { [length: string]: number },
  manualRails: { [length: string]: number }
): FastenerDict {
  const ear = calcResult.earthing;
  const mid = calcResult.middle;
  const edge = calcResult.edge;
  const conn = calcResult.connectors;
  const totalPanels = calcResult.totalPanels;

  let totalLengthCm = 0;

  for (const [lengthStr, qty] of Object.entries(koshrotQty)) {
    const length = parseFloat(lengthStr);
    if (!isNaN(length)) {
      totalLengthCm += length * qty;
    }
  }

  for (const [length, qty] of Object.entries(manualRails)) {
    const lengthNum = parseFloat(String(length));
    if (!isNaN(lengthNum)) {
      totalLengthCm += lengthNum * qty;
    }
  }

  const screwsIso = roundUpToTens(conn * 4 + totalPanels);
  let m8Count = 0;
  if (totalLengthCm > 0) {
    const m8Base = totalLengthCm / 140.0;
    m8Count = roundUpToTens(m8Base);
  }

  return {
    'מהדק הארקה': ear,
    'מהדק אמצע': mid,
    'מהדק קצה': edge,
    'פקק לקושרות': edge,
    'מחברי קושרות': conn,
    'בורג איסכורית 3,5': screwsIso,
    'M8 בורג': m8Count,
    'M8 אום': m8Count,
  };
}
