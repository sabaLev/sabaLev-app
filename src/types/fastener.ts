export interface Fastener {
  label: string;
  value: number;
  included: boolean;
}

export interface FastenerDict {
  [label: string]: number;
}

export interface FastenerInclude {
  [label: string]: boolean;
}
