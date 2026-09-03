/* just imported useState */
import { useState } from 'react';

export default function AddProjectForm({ onAdd }) {
  const [title, setTitle] = useState("");
  const [tech, setTech] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (title.trim() === "" || tech.trim() === "") return;
    onAdd({ title, tech });
    setTitle("");
    setTech("");
  }

  return (
    <form onSubmit={handleSubmit} className="mt-6 flex gap-2">
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Project title"
        className="flex-1 rounded border border-slate-300 px-3 py-2"
      />
      <input
        value={tech}
        onChange={(e) => setTech(e.target.value)}
        placeholder="Tech"
        className="w-32 rounded border border-slate-300 px-3 py-2"
      />
      <button
        type="submit"
        className="rounded bg-slate-800 px-4 py-2 font-medium text-white hover:bg-slate-900"
      >
        Add
      </button>
    </form>
  );
}
