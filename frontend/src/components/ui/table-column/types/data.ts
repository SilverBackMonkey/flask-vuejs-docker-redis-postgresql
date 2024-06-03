import { TableColumn } from './column';

export interface TableDataRow {
  [key: string]: any;
};

export interface TableData {  // eslint-disable-line
  columns: TableColumn[];
  data: TableDataRow[];
}
