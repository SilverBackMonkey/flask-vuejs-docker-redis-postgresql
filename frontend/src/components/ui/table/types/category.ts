export interface TableCategory {
  name: string;
  tableName?: string;
  key: string;
  values: any[];
  editable?: boolean;
  color?: string;
  hidden?: boolean;
}
