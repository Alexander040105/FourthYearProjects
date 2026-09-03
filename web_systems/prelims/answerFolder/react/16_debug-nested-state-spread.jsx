// Problem 16: Debug: Nested State Spread
// Category: React.js — Difficulty: Hard — Type: Debug
// 
// **Problem:**
// The UI does not update when the theme is toggled.
// ```jsx
// const [user, setUser] = useState({ name: 'Ana', prefs: { theme: 'light' } });
// const toggle = () => {
//   user.prefs.theme = 'dark';
//   setUser(user);
// };
// ```
// Fix the toggle so it updates the nested `theme` property immutably.
// 
// 
// **Constraints:**
// Do not mutate the existing `user` object or its `prefs` object.
// 
// 
// **Prelims topic:**
// nested state, immutability, object spread.

// ========================== YOUR ANSWER BELOW ==========================
// Write your React / JSX answer here
