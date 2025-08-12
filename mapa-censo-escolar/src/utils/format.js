export const formatNumber = (num) => {
  if (num === null || num === undefined) return "N/A";
  return new Intl.NumberFormat("pt-BR").format(num);
};