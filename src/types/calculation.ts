export interface AutoRails {
  [length: number]: number;
}

export interface CalculationResult {
  autoRails: AutoRails;
  connectors: number;
  earthing: number;
  middle: number;
  edge: number;
  totalPanels: number;
}

export interface CalcGroupResult {
  segments: number[];
  connectors: number;
  earthing: number;
  middle: number;
  edge: number;
  railsPerRow: number;
}
