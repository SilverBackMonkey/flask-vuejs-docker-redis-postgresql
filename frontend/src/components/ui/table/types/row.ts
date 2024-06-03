export interface TableOverride {
  handler?: Function;
  size?: string;
  weight?: number;
};

export interface TableOverrideObject {
  [key: string]: TableOverride;
}

export interface TableRow {
  name: string;
  key: string;
  showCounter: boolean;
  separate: boolean;
  editable?: boolean;
  handler?: Function;
  size?: string;
  weight?: number;
  override?: TableOverrideObject;
  help?: string;
}
