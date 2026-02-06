export type GroupOrientation = 'עומד' | 'שוכב';

export interface Group {
  panelsCount: number;
  groupsCount: number;
  orientation: GroupOrientation;
}

export interface GroupsInput {
  vertical: Group[];
  horizontal: Group[];
}
