import { useEffect, useState } from "react";
import {
  getProjects,
  createProject,
  toggleProject,
  deleteProject,
} from "./api";
import ProjectCard from "./components/ProjectCard";
import AddProjectForm from "./components/AddProjectForm";

export default function App() {
  const [projects, setProjects] = useState([]);

  /* just added error handling */
  useEffect(() => {
    getProjects().then(setProjects);
  }, []);

  async function handleAdd(project) {
    const created = await createProject(project);
    /* fixed the set state to update using the ... */
    setProjects((p) => [...p, created]);
  }

  async function handleToggle(id) {
    const updated = await toggleProject(id);
    setProjects(projects.map((p) => (p.id === id ? updated : p)));
  }

  async function handleDelete(id) {
    await deleteProject(id);
    setProjects(projects.filter((p) => p.id !== id));
  }

  return (
    <div className="min-h-screen bg-slate-100 py-10">
      <div className="mx-auto max-w-2xl px-4">
        <h1 className="text-3xl font-bold text-slate-800">Project Tracker</h1>
        <p className="mt-1 text-slate-500">A small full-stack demo app.</p>

        <AddProjectForm onAdd={handleAdd} />

        <div className="mt-6 grid grid-cols-1 gap-4">
          {projects.map((p) => (
            <ProjectCard
              key={p.id}
              project={p}
              onToggle={handleToggle}
              onDelete={handleDelete}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
