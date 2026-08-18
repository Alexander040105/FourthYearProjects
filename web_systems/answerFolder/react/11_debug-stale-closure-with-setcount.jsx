// Problem 11: Debug: Stale Closure with setCount
// Category: React.js — Difficulty: Medium — Type: Debug
// 
// **Problem:**
// Rapidly clicking the button only increments by the value that existed when the button was first clicked.
// ```jsx
// function Counter() {
//   const [count, setCount] = useState(0);
//   const increment = () => setTimeout(() => setCount(count + 1), 1000);
//   return <button onClick={increment}>+</button>;
// }
// ```
// Fix the update so it always uses the latest state.
// 
// 
// **Constraints:**
// Use the functional updater form of `setCount`.
// 
// 
// **Prelims topic:**
// `useState` updater, closures.

// ========================== YOUR ANSWER BELOW ==========================
// Write your React / JSX answer here
