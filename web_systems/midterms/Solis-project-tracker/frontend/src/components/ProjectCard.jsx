export default function ProjectCard({ project, onToggle, onDelete }) {
  return (
    <div className="flex items-center justify-between rounded-lg bg-white p-4 shadow">
      <div>
        <h3
          className={
            "text-lg font-semibold " +
            (project.done ? "text-slate-400 line-through" : "text-slate-800")
          }
        >
          {project.title}
        </h3>
        {/* changed from class to className */}
        <p className="text-sm text-slate-500">{project.tech}</p>
      </div>

      <div className="flex gap-2">
        <button
          onClick={() => onToggle(project.id)}
          className="rounded bg-teal-500 px-3 py-1 text-sm font-medium text-white hover:bg-teal-600"
        >
          {project.done ? "Undo" : "Done"}
        </button>
        <button
        /* fixed this into a proper onclick func as it's {onDelete(project.id)} before*/
          onClick={() => onDelete(project.id)}
          className="rounded bg-red-500 px-3 py-1 text-sm font-medium text-white hover:bg-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
