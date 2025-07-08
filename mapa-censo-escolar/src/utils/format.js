export const formatNumber = (num) => {
  if (!num) return "N/A";
  return new Intl.NumberFormat("pt-BR").format(num);
};