import { TableRow } from '@/components/ui/table/types';

import {
  ratio,
  singleRatio,
  money,
  dollars,
  percentage,
  percentageAverage,
  rounded,
} from '@/services/renderers';

export const tableRows: TableRow[] = [
  {
    name: 'Earnings per share',
    key: 'earningsPerShare',
    help: 'Basic (non-diluted) EPS = Net Income (07) / Shares Outstanding (20)',
    showCounter: true,
    separate: false,
    handler: ratio,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Free cash flow per share',
    key: 'freeCashFlowPerShare',
    help: 'FCF per share = Free Cash Flow to the Firm (13) / Shares Outstanding (20)',
    showCounter: true,
    separate: false,
    handler: ratio,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Dividends per share',
    key: 'dividendsPerShare',
    showCounter: true,
    separate: false,
    handler: ratio,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Dividends payout, %',
    key: 'dividendsPayout',
    showCounter: true,
    separate: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Revenue',
    key: 'revenue',
    showCounter: true,
    separate: false,
    handler: dollars,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ㅤ% Change',
    key: 'revenueChange',
    showCounter: true,
    separate: false,
    editable: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Net Income',
    key: 'netIncome',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ㅤ% Margin',
    key: 'margin',
    showCounter: true,
    separate: true,
    editable: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentageAverage,
      },
    },
  },
  {
    name: 'CFO',
    key: 'cashFlowFromOperatingActivities',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ㅤ% Of revenue',
    key: 'percentageCfoOfRevenue',
    showCounter: true,
    separate: false,
    editable: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentageAverage,
      },
    },
  },
  {
    name: 'CAPEX',
    key: 'capex',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ㅤ% Change',
    key: 'capexChange',
    showCounter: true,
    separate: false,
    editable: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentageAverage,
      },
    },
  },
  {
    name: 'FCFF',
    key: 'freeCashFlow',
    help: 'Free Cash Flow to the Firm = Cash Flows from Operating Activities (09) – Capital Expenditures (11)',
    showCounter: true,
    separate: true,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Total assets',
    key: 'totalAssets',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ㅤ% Change',
    key: 'totalAssetsChange',
    showCounter: true,
    separate: false,
    editable: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Total liabilities',
    key: 'totalLiabilities',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ㅤ% Of assets',
    key: 'percentageLiabilitiesOfAssets',
    showCounter: true,
    separate: false,
    editable: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentageAverage,
      },
    },
  },
  {
    name: 'Shareholders Equity',
    key: 'shareholdersEquity',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Net Debt',
    key: 'netDebt',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Shares Outstanding',
    key: 'sharesOutstanding',
    help: 'Shares Outstanding: number of shares outstanding as the difference between issued shares and treasury shares',
    showCounter: true,
    separate: false,
    handler: rounded,
    size: 'var(--font-size-8)',
    weight: 600,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ㅤ% Change',
    key: 'sharesOutstandingChange',
    showCounter: true,
    separate: true,
    editable: true,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ROA',
    key: 'roa',
    showCounter: true,
    separate: false,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'ROE',
    key: 'roe',
    showCounter: true,
    separate: false,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Interest coverage',
    key: 'interestCoverage',
    showCounter: true,
    separate: false,
    handler: ratio,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Dividend Yield',
    key: 'dividendYield',
    showCounter: true,
    separate: false,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'P/E Ratio LTM',
    key: 'priceEarningsRatioLtm',
    showCounter: true,
    separate: false,
    handler: singleRatio,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Stock price range',
    key: 'stockPriceRange',
    showCounter: true,
    separate: false,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Average Market Cap',
    key: 'averageMarketCap',
    showCounter: true,
    separate: false,
    handler: money,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'FCF Yield',
    key: 'freeCashFlowYield',
    showCounter: true,
    separate: false,
    handler: percentage,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
  {
    name: 'Average stock price',
    key: 'averageStockPrice',
    showCounter: true,
    separate: false,
    handler: singleRatio,
    override: {
      '10 year gagr': {
        handler: percentage,
      },
    },
  },
];

export const chartRows = {
  earningsPerShare: {
    axis: 'y-right',
    color: '#9650FB',
  },
  freeCashFlowPerShare: {
    axis: 'y-right',
    color: '#E6D690',
  },
  dividendsPerShare: {
    axis: 'y-right',
    color: '#EFDECD',
  },
  dividendsPayout: {
    axis: 'y-right',
    color: '#A8E4A0',
  },
  revenue: {
    axis: 'y-left',
    color: '#3348FB',
  },
  revenueChange: {
    axis: 'y-right',
    color: '#CD00CD',
  },
  netIncome: {
    axis: 'y-left',
    color: '#37D27F',
  },
  margin: {
    axis: 'y-right',
    color: '#BDDA57',
  },
  cashFlowFromOperatingActivities: {
    axis: 'y-left',
    color: '#4E5754',
  },
  percentageCfoOfRevenue: {
    axis: 'y-right',
    color: '#008080',
  },
  capex: {
    axis: 'y-left',
    color: '#8C4743',
  },
  capexChange: {
    axis: 'y-right',
    color: '#EA899A',
  },
  freeCashFlow: {
    axis: 'y-left',
    color: '#01796F',
  },
  totalAssets: {
    axis: 'y-left',
    color: '#E6A8D7',
  },
  totalAssetsChange: {
    axis: 'y-right',
    color: '#FF7518',
  },
  totalLiabilities: {
    axis: 'y-left',
    color: '#90845B',
  },
  percentageLiabilitiesOfAssets: {
    axis: 'y-right',
    color: '#00A86B',
  },
  shareholdersEquity: {
    axis: 'y-left',
    color: '#8E7962',
  },
  netDebt: {
    axis: 'y-left',
    color: '#71BC78',
  },
  sharesOutstanding: {
    axis: 'y-left',
    color: '#03C03C',
  },
  sharesOutstandingChange: {
    axis: 'y-right',
    color: '#1A153F',
  },
  roa: {
    axis: 'y-right',
    color: '#E97451',
  },
  roe: {
    axis: 'y-right',
    color: '#FFBD88',
  },
  interestCoverage: {
    axis: 'y-right',
    color: '#8E4585',
  },
  dividendYield: {
    axis: 'y-right',
    color: '#D2B48C',
  },
  priceEarningsRatioLtm: {
    axis: 'y-right',
    color: '#FF9966',
  },
  averageMarketCap: {
    axis: 'y-left',
    color: '#9400D3',
  },
  freeCashFlowYield: {
    axis: 'y-right',
    color: '#F3A505',
  },
  averageStockPrice: {
    axis: 'y-left',
    color: '#2A8D9C',
  },
};
