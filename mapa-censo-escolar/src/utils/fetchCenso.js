import { stateNameToNumericCode } from "../constants/estados";

export const fetchCensoData = async (ano, estado = null) => {
  try {
    const baseUrl = "http://127.0.0.1:5000/censoescolar";
    const url = estado
      ? `${baseUrl}/${ano}/${stateNameToNumericCode[estado]}`
      : `${baseUrl}/${ano}`;

    const response = await fetch(url);
    if (!response.ok) throw new Error("Erro ao buscar dados");
    const data = await response.json();

    return estado ? [data] : data;
  } catch (error) {
    console.error("Erro ao buscar dados do censo:", error);
    return [];
  }
};