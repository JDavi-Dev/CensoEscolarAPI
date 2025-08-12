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

export const fetchInstituicoes = async (ano, estado, page = 1, search = "") => {
  try {
    const codEstado = stateNameToNumericCode[estado];
    if (!codEstado) return { data: [], total: 0 };

    const params = new URLSearchParams({
      cod_estado: codEstado,
      page: page.toString(),
      per_page: "100",
    });
    if (search.trim()) {
      params.append("q", search.trim());
    }

    const response = await fetch(
      `http://127.0.0.1:5000/instituicoes/${ano}?${params.toString()}`
    );
    if (!response.ok) throw new Error("Erro ao buscar instituições");

    const data = await response.json();

    return {
      data: data.instituicoes || data,
      total: data.total || data.length
    };
  } catch (error) {
    console.error("Erro ao buscar instituições:", error);
    return { data: [], total: 0 };
  }
};