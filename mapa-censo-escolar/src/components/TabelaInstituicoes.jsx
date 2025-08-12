import { useEffect, useMemo, useState } from "react";
import { Table, Container, Pagination, Form } from "react-bootstrap";
// import Fuse from "fuse.js"
import { fetchInstituicoes } from "../utils/fetchCenso";
import { formatNumber } from "../utils/format";

const perPage = 100;

const TabelaInstituicoes = ({ estado, ano, theme }) => {
  const [instituicoes, setInstituicoes] = useState([]);
  const [totalItems, setTotalItems] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");

  // debounce da pesquisa
  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(searchQuery.trim()), 300);
    return () => clearTimeout(t);
  }, [searchQuery]);

  // Buscar dados sempre que estado, ano, página ou pesquisa mudarem
  useEffect(() => {
    if (!estado || estado === "Todos os estados") {
      setInstituicoes([]);
      setTotalItems(0);
      return;
    }

    let canceled = false;
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const { data, total } = await fetchInstituicoes(
          ano,
          estado,
          currentPage,
          debouncedQuery
        );
        if (!canceled) {
          setInstituicoes(data || []);
          setTotalItems(total || 0);
        }
      } catch (err) {
        console.error("Erro ao buscar instituições:", err);
        if (!canceled) {
          setInstituicoes([]);
          setTotalItems(0);
        }
      } finally {
        if (!canceled) setIsLoading(false);
      }
    };

    fetchData();
    return () => {
      canceled = true;
    };
  }, [estado, ano, currentPage, debouncedQuery]);

  useEffect(() => {
    setCurrentPage(1);
  }, [debouncedQuery, estado, ano]);

  const totalPages = Math.max(1, Math.ceil(totalItems / perPage));

  if (estado === "Todos os estados" || !estado) return null;

  return (
    <Container
      className="mt-4 mb-5"
      style={{
        backgroundColor: theme === "light" ? "white" : "#2c3e50",
        border: theme === "light" ? "none" : "1px solid #3a4a5d",
        borderRadius: "12px",
        padding: "20px",
        boxShadow:
          theme === "light"
            ? "0 4px 6px rgba(0, 0, 0, 0.1)"
            : "0 4px 6px rgba(0, 0, 0, 0.3)",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
          flexWrap: "wrap",
          gap: "10px",
        }}
      >
        <h4
          style={{
            color: theme === "light" ? "#2c3e50" : "#e0e0e0",
            margin: 0,
          }}
        >
          Instituições de Ensino em {estado} ({ano})
        </h4>

        <Form.Control
          className={`search-input ${theme === "dark" ? "search-input-dark" : ""}`}
          type="text"
          placeholder="🔍 Pesquisar..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          aria-label="Pesquisar instituições"
          style={{
            width: "280px",
            backgroundColor: theme === "light" ? "white" : "#445a70",
            color: theme === "light" ? "#212529" : "#e0e0e0",
            border:
              theme === "light" ? "1px solid #ced4da" : "1px solid #5a6a7a",
            borderRadius: "6px",
          }}
        />
      </div>

      <div
        style={{
          overflow: "auto",
          maxHeight: "500px",
          position: "relative",
          border: theme === "light" ? "1px solid #dee2e6" : "1px solid #495057",
          borderRadius: "6px",
        }}
      >
        {isLoading ? (
          <div className="text-center py-4">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Carregando...</span>
            </div>
            <p className="mt-2">Carregando instituições...</p>
          </div>
        ) : (
          <Table
            striped
            bordered
            hover
            style={{
              "--bs-table-bg": theme === "light" ? "white" : "#2c3e50",
              "--bs-table-striped-bg":
                theme === "light" ? "#f8f9fa" : "#364a60",
              "--bs-table-hover-bg": theme === "light" ? "#e9ecef" : "#4a5d72",
              "--bs-table-color": theme === "light" ? "#212529" : "#f0f0f0",
              "--bs-table-striped-color":
                theme === "light" ? "#212529" : "#f0f0f0",
              "--bs-table-hover-color":
                theme === "light" ? "#212529" : "#f0f0f0",
              "--bs-table-border-color":
                theme === "light" ? "#dee2e6" : "#495057",
              marginBottom: 0,
            }}
          >
            <thead
              style={{
                position: "sticky",
                top: 0,
                zIndex: 1,
                backgroundColor: theme === "light" ? "#f8f9fa" : "#1a2b3c",
                color: theme === "light" ? "#212529" : "#e0e0e0",
              }}
            >
              <tr>
                <th>Região</th>
                <th>Município</th>
                <th>Mesorregião</th>
                <th>Microrregião</th>
                <th>Instituição</th>
                <th>Código Instituição</th>
                <th>Matrículas</th>
              </tr>
            </thead>
            <tbody>
              {/* instiuicoes */}
              {instituicoes.length === 0 ? (
                <tr>
                  <td
                    colSpan="7"
                    style={{
                      textAlign: "center",
                      color: theme === "light" ? "#6c757d" : "#adb5bd",
                    }}
                  >
                    Nenhuma instituição encontrada.
                  </td>
                </tr>
              ) : (
                instituicoes.map((instituicao) => (
                  <tr
                    key={`${instituicao.cod_entidade}-${instituicao.ano_censo}`}
                    style={{
                      backgroundColor: theme === "light" ? "white" : "#3a4a5d",
                    }}
                  >
                    <td>{instituicao.regiao}</td>
                    <td>{instituicao.municipio}</td>
                    <td>{instituicao.mesorregiao}</td>
                    <td>{instituicao.microrregiao}</td>
                    <td>{instituicao.entidade}</td>
                    <td>{instituicao.cod_entidade}</td>
                    <td>{formatNumber(instituicao.qt_mat_bas)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </Table>
        )}
      </div>
      <style>
        {`
          .pagination-lg .page-link {
            padding: 0.75rem 1rem;
            font-size: 1.1rem;
            line-height: 1.5;
            min-width: 45px;
          }

          /* Tema escuro */
          .pagination-dark .page-link {
            background-color: #3a4a5d;
            color: #e0e0e0;
            border-color: #495057;
          }
          
          .pagination-dark .page-item.active .page-link {
            background-color: #1a2b3c;
            border-color: #495057;
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
          }
          
          .pagination-dark .page-item.disabled .page-link {
            background-color: #2c3e50;
            color: #6c757d;
            opacity: 0.7;
          }
          
          .pagination-dark .page-link:hover {
            background-color: #495057;
            color: #ffffff;
            transform: translateY(-1.5px);
            transition: transform 0.2s ease;
          }

          .pagination-dark .page-link:focus {
            box-shadow: 0 0 0 0.2rem rgba(58, 74, 93, 0.25);
          }
          
          /* Estilos para o tema claro */
          .pagination-light .page-link {
            background-color: #ffffff;
            color: #3b7ce0;
            border-color: #dee2e6;
            transition: all 0.2s ease;
          }
          
          .pagination-light .page-item.active .page-link {
            background-color: #0074d9;
            color: #ffffff;
            border-color: #dee2e6;
            font-weight: 600;
          }
          
          .pagination-light .page-item.disabled .page-link {
            background-color: #f8f9fa;
            color: #6c757d;
            opacity: 0.7;
          }
          
          .pagination-light .page-link:hover {
            background-color: #e9ecef;
            transform: translateY(-1.5px);
          }

          .search-input-dark::placeholder {
            color: #adb5bd;
          }

          .search-input-dark::-webkit-input-placeholder {
            color: #adb5bd;
          }

          .search-input-dark:-moz-placeholder {
            color: #adb5bd;
            opacity: 1;
          }

          .search-input-dark::-moz-placeholder {
            color: #adb5bd;
            opacity: 1;
          }

          .search-input-dark:-ms-input-placeholder {
            color: #adb5bd;
          }
        `}
      </style>

      {/* Paginação */}
      <div className="d-flex justify-content-center mt-3">
        <Pagination
          className={theme === "dark" ? "pagination-dark" : "pagination-light"}
        >
          <Pagination.First
            onClick={() => setCurrentPage((p) => Math.max(1, p - 10))}
            disabled={currentPage === 1}
          />
          <Pagination.Prev
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
          />

          {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
            let pageNum;
            if (totalPages <= 5) {
              pageNum = i + 1;
            } else if (currentPage <= 3) {
              pageNum = i + 1;
            } else if (currentPage >= totalPages - 2) {
              pageNum = totalPages - 4 + i;
            } else {
              pageNum = currentPage - 2 + i;
            }

            return (
              <Pagination.Item
                key={pageNum}
                active={pageNum === currentPage}
                onClick={() => setCurrentPage(pageNum)}
              >
                {pageNum}
              </Pagination.Item>
            );
          })}

          <Pagination.Next
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
          />
          <Pagination.Last
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 10))}
            disabled={currentPage === totalPages}
          />
        </Pagination>
      </div>

      <div
        style={{
          textAlign: "center",
          color: theme === "light" ? "#6c757d" : "#adb5bd",
          marginTop: "10px",
        }}
      >
        Página {currentPage} de {totalPages} | Total de {totalItems}{" "}
        instituições
      </div>
    </Container>
  );
};

export default TabelaInstituicoes;
