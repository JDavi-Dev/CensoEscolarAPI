import { useState } from "react";
import { Form, Container } from "react-bootstrap";
import { ChevronDown } from "react-bootstrap-icons";
import { estadosPorRegiao } from "../constants/estados";

const Formulario = ({ filters, onFilterChange, theme }) => {
  const [isAnoOpen, setIsAnoOpen] = useState(false);
  const [isEstadoOpen, setIsEstadoOpen] = useState(false);

  const handleAnoChange = (e) => {
    onFilterChange({ ano: e.target.value });
  };

  const handleEstadoChange = (e) => {
    onFilterChange({ estado: e.target.value });
  };

  return (
    <Container
      className="mt-4 mb-4 p-4"
      style={{
        backgroundColor: theme === "light" ? "white" : "#2c3e50",
        border: theme === "light" ? "none" : "1px solid #3a4a5d",
        borderRadius: "12px",
        maxWidth: "700px",
        boxShadow:
          theme === "light"
            ? "0 4px 6px rgba(0, 0, 0, 0.1)"
            : "0 4px 6px rgba(0, 0, 0, 0.3)",
      }}
    >
      <Form
        className="d-flex flex-column flex-md-row"
        style={{
          justifyContent: "center",
          alignItems: "center",
          gap: "20px",
        }}
      >
        <Form.Group
          controlId="ano"
          className="me-md-5"
          style={{ width: 100, position: "relative" }}
        >
          <Form.Label
            style={{
              fontSize: 18,
              fontWeight: "500",
              color: theme === "light" ? "#2c3e50" : "#e0e0e0",
            }}
          >
            Ano:
          </Form.Label>
          <Form.Control
            as="select"
            value={filters.ano}
            onChange={handleAnoChange}
            size="sm"
            title="Selecione o ano do censo escolar"
            aria-label="Selecionar ano do censo escolar"
            role="combobox"
            aria-expanded={isAnoOpen}
            style={{
              fontSize: 14,
              fontWeight: "450",
              appearance: "none",
              paddingRight: "25px",
              border:
                theme === "light" ? "1px solid #ced4da" : "1px solid #5a6a7a",
              borderRadius: "6px",
              cursor: "pointer",
              backgroundColor: theme === "light" ? "white" : "#445a70",
              color: theme === "light" ? "#495057" : "#e0e0e0", // Ajuste de cor do texto
              transition: "all 0.3s ease", // Adiciona transição
              ":hover": {
                borderColor: theme === "light" ? "#adb5bd" : "#7f8c8d", // Efeito hover
              },
              ":focus": {
                borderColor: theme === "light" ? "#3498db" : "#9b59b6",
                boxShadow:
                  theme === "light"
                    ? "0 0 0 0.2rem rgba(52, 152, 219, 0.25)"
                    : "0 0 0 0.2rem rgba(155, 89, 182, 0.25)",
              },
            }}
            onFocus={() => setIsAnoOpen(true)}
            onBlur={() => setIsAnoOpen(false)}
          >
            <option value="2023">2023</option>
            <option value="2024">2024</option>
          </Form.Control>
          <ChevronDown
            style={{
              position: "absolute",
              right: "10px",
              top: "75%",
              transform: isAnoOpen
                ? "translateY(-50%) rotate(180deg)"
                : "translateY(-50%)",
              transition: "transform 0.2s ease-in-out",
              pointerEvents: "none",
              fontSize: "1.1rem",
              color: theme === "light" ? "#495057" : "#bbb",
            }}
            aria-hidden="true"
          />
        </Form.Group>

        <Form.Group
          controlId="estado"
          style={{ width: 185, position: "relative" }}
        >
          <Form.Label
            style={{
              fontSize: 18,
              fontWeight: "500",
              color: theme === "light" ? "#2c3e50" : "#e0e0e0",
            }}
          >
            Estado:
          </Form.Label>
          <Form.Control
            as="select"
            value={filters.estado}
            onChange={handleEstadoChange}
            size="sm"
            title="Selecione um estado ou 'Todos os estados'"
            aria-label="Selecionar estado para visualização"
            role="combobox"
            aria-expanded={isEstadoOpen}
            style={{
              fontSize: 14,
              fontWeight: "450",
              appearance: "none",
              paddingRight: "25px",
              border:
                theme === "light" ? "1px solid #ced4da" : "1px solid #5a6a7a",
              borderRadius: "6px",
              cursor: "pointer",
              backgroundColor: theme === "light" ? "white" : "#445a70",
              color: theme === "light" ? "#495057" : "#e0e0e0",
              transition: "all 0.3s ease",
              ":hover": {
                borderColor: theme === "light" ? "#adb5bd" : "#7f8c8d",
              },
              ":focus": {
                borderColor: theme === "light" ? "#3498db" : "#9b59b6",
                boxShadow:
                  theme === "light"
                    ? "0 0 0 0.2rem rgba(52, 152, 219, 0.25)"
                    : "0 0 0 0.2rem rgba(155, 89, 182, 0.25)",
              },
            }}
            onFocus={() => setIsEstadoOpen(true)}
            onBlur={() => setIsEstadoOpen(false)}
          >
            <option value="Todos os estados">Todos os estados</option>
            {Object.entries(estadosPorRegiao).map(([regiao, estados]) => (
              <optgroup
                label={regiao}
                key={regiao}
                style={{
                  backgroundColor: theme === "light" ? "white" : "#445a70",
                  color: theme === "light" ? "#495057" : "#e0e0e0",
                }}
              >
                {estados.map((estado) => (
                  <option
                    key={estado.codigo}
                    value={estado.nome}
                    title={`Selecionar ${estado.nome}`}
                    style={{
                      backgroundColor: theme === "light" ? "white" : "#445a70",
                      color: theme === "light" ? "#495057" : "#e0e0e0",
                    }}
                  >
                    {estado.nome}
                  </option>
                ))}
              </optgroup>
            ))}
          </Form.Control>
          <ChevronDown
            style={{
              position: "absolute",
              right: "10px",
              top: "75%",
              transform: isEstadoOpen
                ? "translateY(-50%) rotate(180deg)"
                : "translateY(-50%)",
              transition: "transform 0.2s ease-in-out",
              pointerEvents: "none",
              fontSize: "1.1rem",
              color: theme === "light" ? "#495057" : "#bbb",
            }}
            aria-hidden="true"
          />
        </Form.Group>
      </Form>
    </Container>
  );
};

export default Formulario;