export interface Part {
  id?: number;
  name: string;
  unit: string;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface ExtraPart {
  name: string;
  qty: number;
}
