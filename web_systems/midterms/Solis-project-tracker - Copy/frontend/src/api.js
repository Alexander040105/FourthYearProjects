// One place for every call to the FastAPI back end.
const BASE = "http://localhost:8000";

export async function getProjects() {
  const res = await fetch(`${BASE}/projects`);
  return res.json();
}

export async function createProject(project) {
  const res = await fetch(`${BASE}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(project),
  });
  return res.json();
}

export async function toggleProject(id) {
  const res = await fetch(`${BASE}/projects/${id}`, { method: "PATCH" });
  return res.json();
}

export async function deleteProject(id) {
  await fetch(`${BASE}/projects/${id}`, { method: "DELETE" });
}
