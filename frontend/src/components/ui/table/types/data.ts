import { TableCategory } from './category';
import { TableRow } from './row';

import { Comment } from '@/rest-api/comments/assets';

export interface TableData {
  categories: TableCategory[];
  rows: TableRow[];
  column: string;
  columnName: string;
  comments?: Comment[];
  hideCategories?: boolean;
  editEvent?: boolean;
}
