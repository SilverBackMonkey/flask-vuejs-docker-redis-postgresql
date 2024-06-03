export const negative = (value: number): string => {
  if (value < 0) {
    return `(${Math.abs(value).toLocaleString()})`;
  }
  return value.toLocaleString();
};

export const round = (value: number): string => negative(Math.round(value));

export const numeric = (value: number): string => {
  const rounded = Math.floor(value / 1_000_000);

  return negative(rounded);
};

export const ratio = (value: number): string => negative(Math.round(value * 100) / 100);

export const percentage = (value: number): string => `${ratio(value)} %`;

export const usd = (value: number): string => `$ ${numeric(value)}`;
