export default function IncidentList({ incidents }) {
  return (
    <section className="card">
      <h2>Historial de incidentes</h2>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Titulo</th>
              <th>Tipo</th>
              <th>Severidad</th>
              <th>Estado</th>
              <th>Estudiante</th>
              <th>Curso</th>
              <th>Reportado por</th>
              <th>Fecha incidente</th>
            </tr>
          </thead>
          <tbody>
            {incidents.map((incident) => (
              <tr key={incident.id}>
                <td>{incident.title}</td>
                <td>{incident.incident_type}</td>
                <td>{incident.severity}</td>
                <td>{incident.status}</td>
                <td>{incident.student_name}</td>
                <td>{incident.course}</td>
                <td>{incident.reported_by}</td>
                <td>{new Date(incident.occurred_at).toLocaleString()}</td>
              </tr>
            ))}
            {!incidents.length && (
              <tr>
                <td colSpan={8}>No hay incidentes registrados con los filtros actuales.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
