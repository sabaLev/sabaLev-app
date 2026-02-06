export interface Panel {
  id?: number;
  name: string;
  width: number;
  height: number;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface PanelRow {
  name: string;
  width: number;
  height: number;
}
