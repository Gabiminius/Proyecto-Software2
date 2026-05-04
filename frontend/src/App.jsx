import { useEffect, useMemo, useState } from "react";

import { createIncident, getIncidents } from "./api/incidents";
import IncidentForm from "./components/IncidentForm";
import IncidentList from "./components/IncidentList";

const defaultFilters = {
  incident_type: "",
  status: "",
  course: "",
  student_name: "",
  search: "",
};

export default function App() {
  const [incidents, setIncidents] = useState([]);
  const [filters, setFilters] = useState(defaultFilters);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const cleanFilters = useMemo(() => {
    return Object.fromEntries(Object.entries(filters).filter(([, value]) => value));
  }, [filters]);

  useEffect(() => {
    const loadIncidents = async () => {
      try {
        setIsLoading(true);
        const data = await getIncidents(cleanFilters);
        setIncidents(data);
        setError("");
      } catch {
        setError("No fue posible cargar el historial de incidentes.");
      } finally {
        setIsLoading(false);
      }
    };

    loadIncidents();
  }, [cleanFilters]);

  const handleRegisterIncident = async (payload) => {
    setIsSubmitting(true);
    try {
      const normalizedPayload = {
        ...payload,
        occurred_at: new Date(payload.occurred_at).toISOString(),
      };

      await createIncident(normalizedPayload);
      const data = await getIncidents(cleanFilters);
      setIncidents(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <main className="layout">
      <header>
        <h1>Sistema de Registro de Incidentes Escolares</h1>
        <p>Template escalable con FastAPI + React + Neon PostgreSQL.</p>
      </header>

      <IncidentForm onSubmit={handleRegisterIncident} isSubmitting={isSubmitting} />

      <section className="card filters">
        <h2>Filtros</h2>
        <div className="filter-grid">
          <label>
            Buscar
            <input name="search" value={filters.search} onChange={handleFilterChange} placeholder="Titulo o descripcion" />
          </label>

          <label>
            Tipo
            <select name="incident_type" value={filters.incident_type} onChange={handleFilterChange}>
              <option value="">Todos</option>
              <option value="convivencia">Convivencia</option>
              <option value="disciplina">Disciplina</option>
              <option value="acoso">Acoso</option>
              <option value="seguridad">Seguridad</option>
              <option value="otro">Otro</option>
            </select>
          </label>

          <label>
            Estado
            <select name="status" value={filters.status} onChange={handleFilterChange}>
              <option value="">Todos</option>
              <option value="abierto">Abierto</option>
              <option value="en_revision">En revision</option>
              <option value="resuelto">Resuelto</option>
              <option value="cerrado">Cerrado</option>
            </select>
          </label>

          <label>
            Curso
            <input name="course" value={filters.course} onChange={handleFilterChange} />
          </label>

          <label>
            Estudiante
            <input name="student_name" value={filters.student_name} onChange={handleFilterChange} />
          </label>
        </div>
      </section>

      {error ? <p className="error">{error}</p> : null}
      {isLoading ? <p>Cargando...</p> : <IncidentList incidents={incidents} />}
    </main>
  );
}
