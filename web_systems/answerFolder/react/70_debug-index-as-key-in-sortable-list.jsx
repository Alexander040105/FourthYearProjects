// Problem 70: Debug: Index as Key in Sortable List
// Category: React.js — Difficulty: Hard — Type: Debug
// 
// **Problem:**
// This list uses the array index as the key. It causes subtle bugs when the list is reordered or filtered:
// ```jsx
// <ul>
//   {projects.map((p, index) => (
//     <li key={index}>{p.title}</li>
//   ))}
// </ul>
// ```
// Rewrite it to use a stable key and explain why the index is risky.
// 
// 
// 
// **Constraints:**
// - Use `p.id` (a stable value from the data) as the key.
// - Explain the bug in a comment or short paragraph.
// 
// 
// 
// **Prelims topic:**
// Keys, list rendering, reconciliation.

// ========================== YOUR ANSWER BELOW ==========================
// Write your React / JSX answer here
