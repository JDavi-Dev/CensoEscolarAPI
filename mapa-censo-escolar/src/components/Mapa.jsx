import { useState, useEffect, useMemo } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
} from "react-simple-maps";
import Formulario from "./Formulario";
import { SunFill, MoonFill } from "react-bootstrap-icons";
import { stateNameToCode } from "../constants/estados";
import { fetchCensoData } from "../utils/fetchCenso";
import { formatNumber } from "../utils/format";

const geoUrl =
  "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson";

const stateMarkers = [
  { name: "AC", coordinates: [-70.268555, -9.18887] },
  { name: "AL", coordinates: [-36.386719, -9.953972] },
  { name: "AM", coordinates: [-64.291992, -4.565474] },
  { name: "AP", coordinates: [-52.075195, 0.966751] },
  { name: "BA", coordinates: [-41.5, -12.5] },
  { name: "CE", coordinates: [-39.5, -5.5] },
  { name: "DF", coordinates: [-47.5, -15.5] },
  { name: "ES", coordinates: [-40.5, -20] },
  { name: "GO", coordinates: [-50.097656, -16.495349] },
  { name: "MA", coordinates: [-45, -5] },
  { name: "MG", coordinates: [-44.428711, -18.798418] },
  { name: "MS", coordinates: [-54.5, -20.5] },
  { name: "MT", coordinates: [-56, -13.5] },
  { name: "PA", coordinates: [-53.129883, -5.090944] },
  { name: "PB", coordinates: [-36.166992, -7.391067] },
  { name: "PE", coordinates: [-38.012695, -8.522626] },
  { name: "PI", coordinates: [-42.275391, -7.957237] },
  { name: "PR", coordinates: [-51.987305, -24.872732] },
  { name: "RJ", coordinates: [-42.8, -22.5] },
  { name: "RN", coordinates: [-36.5, -5.8] },
  { name: "RO", coordinates: [-63.039551, -11.307708] },
  { name: "RR", coordinates: [-61, 2] },
  { name: "RS", coordinates: [-53, -30] },
  { name: "SC", coordinates: [-50.141602, -27.76133] },
  { name: "SE", coordinates: [-37.353516, -10.947933] },
  { name: "SP", coordinates: [-48.647461, -22.74199] },
  { name: "TO", coordinates: [-48.449707, -10.271681] },
];

const Mapa = () => {
  const [censoData, setCensoData] = useState([]);
  const [filters, setFilters] = useState({
    ano: "2023",
    estado: "Todos os estados",
  });
  const [hoveredState, setHoveredState] = useState(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [showTooltip, setShowTooltip] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState("light");

  // Mapeamento de siglas para nomes completos
  const codeToStateName = useMemo(() => {
    return Object.fromEntries(
      Object.entries(stateNameToCode).map(([name, code]) => [code, name])
    );
  }, []);

  useEffect(() => {
    const buscar = async () => {
      setIsLoading(true);
      const data = await fetchCensoData(
        filters.ano,
        filters.estado === "Todos os estados" ? null : filters.estado
      );
      setCensoData(data);
      setIsLoading(false);
    };
    buscar();
  }, [filters]);

  const handleFilterChange = (newFilters) => {
    setFilters((prevFilters) => ({
      ...prevFilters,
      ...newFilters,
    }));
  };

  const getCensoValueForState = (stateName) => {
    const sigla = stateNameToCode[stateName];
    if (!sigla) return null;

    const estadoData = censoData.find((item) => item.sigla === sigla);
    return estadoData ? estadoData.total_matriculas : null;
  };

  const getColorForValue = (value, maxValue) => {
    if (value === null) return "#5a6a7a";
    const intensity = Math.sqrt(value / maxValue);
    return theme === "dark"
      ? `hsl(280, 45%, ${80 - intensity * 50}%)`
      : `hsl(210, 80%, ${90 - intensity * 50}%)`;
  };

  const maxValue = useMemo(
    () => Math.max(...censoData.map((item) => item.total_matriculas || 0), 0),
    [censoData]
  );

  const handleMouseMove = (geo, event) => {
    const stateName = geo.properties.name;
    if (getCensoValueForState(stateName) !== null) {
      setHoveredState(stateName);
      setTooltipPosition({ x: event.clientX + 30, y: event.clientY + 5 });
      setShowTooltip(true);
    } else {
      setShowTooltip(false);
    }
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
    setHoveredState(null);
  };

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  return (
    <div
      style={{
        background:
          theme === "light"
            ? "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
            : "linear-gradient(135deg, #2c3e50 0%, #1a2b3c 100%)",
        minHeight: "100vh",
        padding: "20px",
        color: theme === "light" ? "#333" : "#eee",
        transition: "background 0.5s ease, color 0.3s ease",
      }}
    >
      <button
        onClick={toggleTheme}
        title={theme === "light" ? "Ativar modo escuro" : "Ativar modo claro"}
        aria-label={theme === "light" ? "Mudar para tema escuro" : "Mudar para tema claro"}
        role="switch"
        aria-checked={theme === "dark"}
        style={{
          position: "fixed",
          top: "25px",
          right: "30px",
          borderRadius: "50%",
          border: "none",
          backgroundColor: theme === "light" ? "#3498db" : "#9b59b6",
          color: "white",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          width: "50px",
          height: "50px",
          boxShadow: "0 2px 4px rgba(0,0,0,0.2)",
          zIndex: 1000,
          transition: "background-color 0.3s ease",
        }}
      >
        {theme === "light" ? <MoonFill size={24} aria-hidden="true"/> : <SunFill size={24} aria-hidden="true"/>}
      </button>
      <div
        style={{ textAlign: "center", marginTop: "20px", marginBottom: "20px" }}
      >
        <h2
          style={{
            fontWeight: "600",
            color: theme === "light" ? "#2c3e50" : "#e0e0e0",
            margin: "20px 0",
            fontSize: "2rem",
            textShadow: "1px 1px 2px rgba(0,0,0,0.1)",
          }}
        >
          🇧🇷 Mapa do Censo Escolar 📚
        </h2>
      </div>
      <Formulario
        filters={filters}
        onFilterChange={handleFilterChange}
        theme={theme}
      />{" "}
      {/* Passando a prop theme */}
      {isLoading && (
        <>
          <div
            style={{
              position: "fixed",
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: "rgba(0, 0, 0, 0.2)",
              zIndex: 999,
            }}
          />
          <div
            style={{
              position: "fixed",
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%)",
              zIndex: 1000,
              backgroundColor:
                theme === "light"
                  ? "rgba(255, 255, 255, 0.8)"
                  : "rgba(44, 62, 80, 0.8)",
              padding: "12px 15px",
              borderRadius: "8px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
              border: theme === "light" ? "1px solid #eee" : "1px solid #555",
            }}
          >
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Carregando...</span>
            </div>
            <p
              style={{
                marginTop: "10px",
                color: theme === "light" ? "#2c3e50" : "#e0e0e0",
                fontWeight: "500",
              }}
            >
              Carregando dados...
            </p>
          </div>
        </>
      )}
      {filters.estado !== "Todos os estados" && censoData.length > 0 && (
        <div
          style={{
            width: "100%",
            display: "flex",
            justifyContent: "center",
            marginTop: "22px",
            marginBottom: "1px",
          }}
        >
          <div
            style={{
              textAlign: "center",
              fontSize: "16px",
              fontWeight: "500",
              padding: "12px 24px",
              backgroundColor: theme === "light" ? "#2c3e50" : "#1a2b3c",
              color: "white",
              borderRadius: "8px",
              boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
              margin: "20px auto",
              maxWidth: "80%",
            }}
          >
            {`${filters.estado} (${filters.ano}) - Matrículas: ${formatNumber(
              censoData[0]?.total_matriculas
            )}`}
          </div>
        </div>
      )}
      <div
        style={{
          width: "100%",
          maxWidth: "900px",
          margin: "20px auto",
          position: "relative",
          backgroundColor: theme === "light" ? "white" : "#2c3e50",
          border: theme === "light" ? "none" : "1px solid #3a4a5d",
          borderRadius: "12px",
          boxShadow:
            theme === "light"
              ? "0 4px 12px rgba(0, 0, 0, 0.15)"
              : "0 4px 12px rgba(0, 0, 0, 0.35)",
        }}
      >
        <ComposableMap
          projection="geoMercator"
          projectionConfig={{
            center: [-54, -15],
            scale: 725,
          }}
          style={{ width: "100%", height: "auto" }}
        >
          <Geographies geography={geoUrl}>
            {({ geographies }) =>
              geographies.map((geo) => {
                const stateName = geo.properties.name;
                const censoValue = getCensoValueForState(stateName);
                const isSelectedState =
                  filters.estado !== "Todos os estados" &&
                  stateName === filters.estado;

                let fillColor;
                if (filters.estado === "Todos os estados") {
                  fillColor = getColorForValue(censoValue, maxValue);
                } else {
                  fillColor = isSelectedState
                    ? theme === "light"
                      ? "#449be0"
                      : "#3F51B5"
                    : theme === "light"
                    ? "#EAEAEC"
                    : "#5a6a7a";
                }

                return (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill={fillColor}
                    stroke={theme === "light" ? "#D6D6DA" : "#778899"}
                    strokeWidth={0.5}
                    style={{
                      default: { outline: "none" },
                      hover: {
                        fill: isSelectedState
                          ? theme === "light"
                            ? "#4da8f0"
                            : "#5C6BC0"
                          : theme === "light"
                          ? "#6a4c93"
                          : "#4db6ac",
                        outline: "none",
                        cursor: "pointer",
                        transition: "fill 0.3s ease",
                      },
                      pressed: {
                        fill: theme === "light" ? "#1976d2" : "#303F9F",
                        outline: "none",
                      },
                    }}
                    onMouseMove={(event) => handleMouseMove(geo, event)}
                    onMouseLeave={handleMouseLeave}
                  />
                );
              })
            }
          </Geographies>

          {stateMarkers.map(({ name, coordinates }) => (
            <Marker key={name} coordinates={coordinates}>
              <text
                textAnchor="middle"
                y="0"
                style={{
                  fontFamily: "Arial, sans-serif",
                  fill: theme === "light" ? "#333" : "#c0e0c0",
                  fontSize: "10px",
                  fontWeight: "bold",
                  pointerEvents: "none",
                  textShadow:
                    theme === "dark" ? "0 0 2px rgba(0,0,0,0.7)" : "none",
                }}
              >
                {name}
              </text>
            </Marker>
          ))}
        </ComposableMap>

        {showTooltip && hoveredState && (
          <div
            style={{
              position: "fixed",
              left: `${tooltipPosition.x}px`,
              top: `${tooltipPosition.y}px`,
              backgroundColor: theme === "light" ? "#2c3e50" : "#1a2b3c",
              color: "white",
              padding: "8px 12px",
              borderRadius: "6px",
              boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
              zIndex: 100,
              pointerEvents: "none",
              fontSize: "14px",
              fontWeight: "500",
              transform: "translateY(-50%)",
              whiteSpace: "nowrap",
              borderLeft:
                theme === "light" ? "4px solid #3498db" : "4px solid #9b59b6",
            }}
          >
            {`${hoveredState}: ${formatNumber(
              getCensoValueForState(hoveredState)
            )}`}
          </div>
        )}
        <div
          style={{
            position: "absolute",
            left: "40px",
            bottom: "35px",
            backgroundColor:
              theme === "light"
                ? "rgba(255, 255, 255, 0.9)"
                : "rgba(52, 73, 94, 0.9)",
            padding: "12px",
            borderRadius: "8px",
            boxShadow:
              theme === "light"
                ? "0 2px 8px rgba(0,0,0,0.15)"
                : "0 2px 8px rgba(0,0,0,0.35)",
            zIndex: 10,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            border: theme === "light" ? "1px solid #eee" : "1px solid #666",
          }}
        >
          <div
            style={{
              fontSize: "12px",
              fontWeight: "600",
              marginBottom: "8px",
              color: theme === "light" ? "#2c3e50" : "#e0e0e0",
            }}
          >
            Matrículas
          </div>

          {/* Escala de cores */}
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              height: "150px",
              justifyContent: "space-between",
            }}
          >
            <span
              style={{
                fontSize: "11px",
                color: theme === "light" ? "#333" : "#eee",
              }}
            >
              Mais
            </span>

            {[1, 0.75, 0.5, 0.25, 0].map((val) => (
              <div
                key={val}
                style={{
                  width: "20px",
                  height: "20px",
                  backgroundColor: getColorForValue(maxValue * val, maxValue),
                  borderRadius: "3px",
                  border:
                    theme === "light" ? "1px solid #ddd" : "1px solid #888",
                }}
              />
            ))}

            <span
              style={{
                fontSize: "11px",
                color: theme === "light" ? "#333" : "#eee",
              }}
            >
              Menos
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Mapa;