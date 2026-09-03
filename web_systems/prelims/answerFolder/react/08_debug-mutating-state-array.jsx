// Problem 8: Debug: Mutating State Array
// Category: React.js — Difficulty: Medium — Type: Debug
// 
// **Problem:**
// The UI does not update when `add` is called.
// ```jsx
// export default function TodoList() {
//   const [todos, setTodos] = useState(['Buy milk']);
//   const add = () => {
//     todos.push('Walk dog');
//     setTodos(todos);
//   };
//   return (
//     <>
//       <ul>{todos.map((t, i) => <li key={i}>{t}</li>)}</ul>
//       <button onClick={add}>Add</button>
//     </>
//   );
// }
// ```
// Fix the state update so React re-renders correctly.
// 
// 
// **Constraints:**
// Do not mutate state directly.
// 
// 
// **Prelims topic:**
// immutable state updates, arrays in state.

// ========================== YOUR ANSWER BELOW ==========================
// Write your React / JSX answer here
