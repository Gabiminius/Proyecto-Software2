import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
});

export async function getIncidents(filters = {}) {
  const { data } = await api.get("/incidents", { params: filters });
  return data;
}

export async function createIncident(payload) {
  const { data } = await api.post("/incidents", payload);
  return data;
}
