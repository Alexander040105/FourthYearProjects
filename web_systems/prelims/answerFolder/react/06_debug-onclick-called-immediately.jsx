// Problem 6: Debug: onClick Called Immediately
// Category: React.js — Difficulty: Easy — Type: Debug
// 
// **Problem:**
// This code either crashes or re-renders in a loop.
// ```jsx
// export default function App() {
//   const [count, setCount] = useState(0);
//   return <button onClick={setCount(count + 1)}>Click</button>;
// }
// ```
// Fix the `onClick` so it calls the updater correctly when the button is clicked.
// 
// 
// **Constraints:**
// `onClick` must receive a function, not a function call.
// 
// 
// **Prelims topic:**
// event handlers, camelCase `onClick`.

// ========================== YOUR ANSWER BELOW ==========================
// Write your React / JSX answer here
