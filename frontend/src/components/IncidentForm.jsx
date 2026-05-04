import { useMemo, useState } from "react";

const initialForm = {
  title: "",
  description: "",
  incident_type: "convivencia",
  severity: "media",
  reported_by: "",
  student_name: "",
  course: "",
  occurred_at: "",
};

function getSubmitErrorMessage(submitError) {
  const detail = submitError?.response?.data?.detail;

  if (typeof detail === "string" && detail.trim()) {
    return detail;
  }

  if (Array.isArray(detail) && detail.length > 0) {
    const firstError = detail[0];
    const field = Array.isArray(firstError?.loc)
      ? firstError.loc.filter((part) => part !== "body").join(".")
      : "";
    const message = typeof firstError?.msg === "string" ? firstError.msg : "Datos invalidos";
    return field ? `${field}: ${message}` : message;
  }

  if (typeof submitError?.message === "string" && submitError.message.trim()) {
    return submitError.message;
  }

  return "No se pudo registrar el incidente.";
}

export default function IncidentForm({ onSubmit, isSubmitting }) {
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState("");

  const canSubmit = useMemo(() => {
    return (
      form.title.trim().length >= 5 &&
      form.description.trim().length >= 10 &&
      form.reported_by.trim().length >= 3 &&
      form.student_name.trim().length >= 3 &&
      form.course.trim().length >= 2 &&
      Boolean(form.occurred_at)
    );
  }, [form]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");

    try {
      await onSubmit(form);
      setForm(initialForm);
    } catch (submitError) {
      setError(getSubmitErrorMessage(submitError));
    }
  };

  return (
    <form className="card form-grid" onSubmit={handleSubmit}>
      <h2>Nuevo incidente</h2>

      <label>
        Titulo
        <input name="title" value={form.title} onChange={handleChange} required />
      </label>

      <label>
        Descripcion
        <textarea name="description" value={form.description} onChange={handleChange} required rows={4} />
      </label>

      <label>
        Tipo
        <select name="incident_type" value={form.incident_type} onChange={handleChange}>
          <option value="convivencia">Convivencia</option>
          <option value="disciplina">Disciplina</option>
          <option value="acoso">Acoso</option>
          <option value="seguridad">Seguridad</option>
          <option value="otro">Otro</option>
        </select>
      </label>

      <label>
        Severidad
        <select name="severity" value={form.severity} onChange={handleChange}>
          <option value="baja">Baja</option>
          <option value="media">Media</option>
          <option value="alta">Alta</option>
          <option value="critica">Critica</option>
        </select>
      </label>

      <label>
        Reportado por
        <input name="reported_by" value={form.reported_by} onChange={handleChange} required />
      </label>

      <label>
        Estudiante
        <input name="student_name" value={form.student_name} onChange={handleChange} required />
      </label>

      <label>
        Curso
        <input name="course" value={form.course} onChange={handleChange} required />
      </label>

      <label>
        Fecha y hora del incidente
        <input type="datetime-local" name="occurred_at" value={form.occurred_at} onChange={handleChange} required />
      </label>

      {error ? <p className="error">{error}</p> : null}

      <button type="submit" disabled={!canSubmit || isSubmitting}>
        {isSubmitting ? "Guardando..." : "Registrar incidente"}
      </button>
    </form>
  );
}
