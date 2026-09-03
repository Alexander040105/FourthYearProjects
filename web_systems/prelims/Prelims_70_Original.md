# 70 Original Prelims Problems (Roulette Edition)

A set of **original** LeetCode-style problems, debug exercises, and build tasks drawn from the prelims reviewer topics. Spin the wheel, pick a number, and solve it.

## How to Use

1. Pick a number from the spin list below.
2. Find that number under the matching category and difficulty.
3. Solve the problem, fix the bug, or build the requested component/app.

## Spin-the-Wheel Index

1. Counter Component — React.js — Easy — Build
2. Debug: Class vs className — React.js — Easy — Debug
3. Fruit List with Keys — React.js — Easy — Build
4. Debug: Adjacent JSX Elements — React.js — Easy — Debug
5. Dynamic Title — React.js — Easy — Build
6. Debug: onClick Called Immediately — React.js — Easy — Debug
7. Filterable Project List — React.js — Medium — Build
8. Debug: Mutating State Array — React.js — Medium — Debug
9. Reusable Button Component — React.js — Medium — Build
10. Multi-Input Registration Form — React.js — Medium — Build
11. Debug: Stale Closure with setCount — React.js — Medium — Debug
12. Tab Switcher — React.js — Medium — Build
13. Shopping Cart — React.js — Hard — Build
14. Debug: Missing List Keys — React.js — Hard — Debug
15. Multi-Step Wizard — React.js — Hard — Build
16. Debug: Nested State Spread — React.js — Hard — Debug
17. Tailwind Card with Children — React.js — Hard — Build
18. Debug: CSS Not Applied — CSS & Tailwind — Easy — Debug
19. Basic Text Styles — CSS & Tailwind — Easy — Build
20. Tailwind Card Utilities — CSS & Tailwind — Easy — Build
21. Debug: Specificity Loses — CSS & Tailwind — Easy — Debug
22. Flexbox Centering — CSS & Tailwind — Easy — Build
23. Debug: Box Model Overflow — CSS & Tailwind — Easy — Debug
24. Responsive Nav Bar — CSS & Tailwind — Medium — Build
25. Debug: Tailwind `class` in JSX — CSS & Tailwind — Medium — Debug
26. Responsive Card Gallery — CSS & Tailwind — Medium — Build
27. Debug: Missing Viewport Meta — CSS & Tailwind — Medium — Debug
28. CSS Custom Properties Theme — CSS & Tailwind — Medium — Build
29. Accessible Form Styling — CSS & Tailwind — Medium — Build
30. Full Landing Page with Tailwind — CSS & Tailwind — Hard — Build
31. Debug: Bootstrap vs Tailwind Conflict — CSS & Tailwind — Hard — Debug
32. Dashboard Layout — CSS & Tailwind — Hard — Build
33. Debug: Specificity War — CSS & Tailwind — Hard — Debug
34. Convert Plain CSS to Tailwind — CSS & Tailwind — Hard — Build
35. FastAPI Hello World — Python & FastAPI — Easy — Build
36. Debug: Python Indentation — Python & FastAPI — Easy — Debug
37. Student Info in Python — Python & FastAPI — Easy — Build
38. GET /projects List — Python & FastAPI — Easy — Build
39. Path Parameter Route — Python & FastAPI — Easy — Build
40. Debug: Create Returns 200 Not 201 — Python & FastAPI — Medium — Debug
41. POST with Pydantic — Python & FastAPI — Medium — Build
42. Query Parameters — Python & FastAPI — Medium — Build
43. Debug: 404 as Normal Body — Python & FastAPI — Medium — Debug
44. In-Memory CRUD API — Python & FastAPI — Medium — Build
45. Nested Pydantic Body — Python & FastAPI — Hard — Build
46. Debug: Type Hint Rejection — Python & FastAPI — Hard — Debug
47. Complete FastAPI App with Docs — Python & FastAPI — Hard — Build
48. Group and Sort Projects — Python & FastAPI — Hard — Build
49. Debug: Broken DELETE and POST ID — Python & FastAPI — Hard — Debug
50. Full FastAPI App with Validation and Errors — Python & FastAPI — Hard — Build
51. Semantic Portfolio Skeleton — HTML, Accessibility & Deployment — Easy — Build
52. Debug: Div Soup to Semantic — HTML, Accessibility & Deployment — Easy — Debug
53. Debug: Broken Heading Hierarchy — HTML, Accessibility & Deployment — Easy — Debug
54. Build: Article with Figure — HTML, Accessibility & Deployment — Easy — Build
55. Debug: Missing Lang and Viewport — HTML, Accessibility & Deployment — Easy — Debug
56. Build: Accessible Contact Form — HTML, Accessibility & Deployment — Medium — Build
57. Debug: Bad Alt Text and Missing Labels — HTML, Accessibility & Deployment — Medium — Debug
58. Build: Accessible Landing Page — HTML, Accessibility & Deployment — Medium — Build
59. Deployment: Push-to-Publish Pipeline — HTML, Accessibility & Deployment — Hard — Build
60. Debug: Broken Images on Live Site — HTML, Accessibility & Deployment — Hard — Debug
61. Debug: Self-Closing Tags in JSX — React.js — Easy — Debug
62. Build: Greeting Card with Props — React.js — Easy — Build
63. Debug: Lowercase Component Name — React.js — Easy — Debug
64. Debug: Missing Curly Braces in JSX — React.js — Medium — Debug
65. Build: Project List with Props and Keys — React.js — Medium — Build
66. Debug: Mutating Props Directly — React.js — Medium — Debug
67. Build: Controlled Name Input — React.js — Medium — Build
68. Build: Toggle Contact Details — React.js — Hard — Build
69. Build: Week 2 Portfolio in React — React.js — Hard — Build
70. Debug: Index as Key in Sortable List — React.js — Hard — Debug

---

## React.js

### Easy

#### 1. Counter Component

**Category:** React.js — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a React component named `Counter` that starts at `0` and shows a paragraph `You have clicked the button {count} times.`. Add a button with an `onClick` handler that increments the count. Use a React Fragment instead of wrapping the returned elements in a `<div>`.


**Example:**
After 3 clicks, the page should display:
```
You have clicked the button 3 times.
```


**Constraints:**
- Root component name must be PascalCase.
- Use `useState` and an `onClick` function.
- Do not mutate state directly.


**Prelims topic:**
`useState`, JSX, React Fragment, event handlers.

---

#### 2. Debug: Class vs className

**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Problem:**
The following component throws a React warning about an invalid DOM property.
```jsx
export default function App() {
  return <h1 class="title">Hello</h1>;
}
```
Fix the attribute used for CSS classes in JSX, and add a Tailwind class `text-navy` so both `title` and the color utility are applied.


**Constraints:**
Use `className`, not `class`, inside JSX.


**Prelims topic:**
`className` vs `class`, Tailwind classes in React.

---

#### 3. Fruit List with Keys

**Category:** React.js — **Difficulty:** Easy — **Type:** Build

**Problem:**
Given the array:
```js
const fruits = ['Apple', 'Banana', 'Orange'];
```
Write a `FruitList` component that renders each fruit as an `<li>` inside a `<ul>`. Use `map()` and provide a unique `key` prop for every list item.


**Example output:**
```html
<ul>
  <li>Apple</li>
  <li>Banana</li>
  <li>Orange</li>
</ul>
```


**Constraints:**
- Use `map()` to render the list.
- Each `<li>` must have a `key` prop.


**Prelims topic:**
list rendering, the `key` prop.

---

#### 4. Debug: Adjacent JSX Elements

**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Problem:**
This component fails to compile.
```jsx
export default function App() {
  return (
    <h1>Title</h1>
    <p>Subtitle</p>
  );
}
```
Fix it by wrapping the adjacent elements in a React Fragment without adding an extra `<div>`.


**Constraints:**
Do not wrap in `<div>`.


**Prelims topic:**
React Fragment (`<>...</>`).

---

#### 5. Dynamic Title

**Category:** React.js — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a React component `App` that stores the page title in a variable and renders:
```html
<header>
  <h1>{title}</h1>
</header>
<main>
  <p>Welcome to {title}</p>
</main>
```
The title should come from a JavaScript variable and be embedded using curly braces.


**Example:**
If `title = "My React App"`, the page shows an `<h1>` and a `<p>` both containing that title.


**Constraints:**
Use a JS expression inside `{ }`.


**Prelims topic:**
dynamic JavaScript expressions in JSX.

---

#### 6. Debug: onClick Called Immediately

**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Problem:**
This code either crashes or re-renders in a loop.
```jsx
export default function App() {
  const [count, setCount] = useState(0);
  return <button onClick={setCount(count + 1)}>Click</button>;
}
```
Fix the `onClick` so it calls the updater correctly when the button is clicked.


**Constraints:**
`onClick` must receive a function, not a function call.


**Prelims topic:**
event handlers, camelCase `onClick`.

---

### Medium

#### 7. Filterable Project List

**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build a `ProjectList` component that receives an array of project objects `{id, title, tech}` and renders them. Add an `<input>` search box that filters the list by `title` or `tech` (case-insensitive) as the user types.


**Example:**
Given `[{id:1, title:"Weather App", tech:"React"}, {id:2, title:"Inventory", tech:"FastAPI"}]` and the search term `"React"`, only the Weather App card is shown.


**Constraints:**
- Use `useState` for the search term.
- Use `filter()` on the projects array.
- Each rendered item must have a `key`.


**Prelims topic:**
controlled input, `filter()`, list rendering.

---

#### 8. Debug: Mutating State Array

**Category:** React.js — **Difficulty:** Medium — **Type:** Debug

**Problem:**
The UI does not update when `add` is called.
```jsx
export default function TodoList() {
  const [todos, setTodos] = useState(['Buy milk']);
  const add = () => {
    todos.push('Walk dog');
    setTodos(todos);
  };
  return (
    <>
      <ul>{todos.map((t, i) => <li key={i}>{t}</li>)}</ul>
      <button onClick={add}>Add</button>
    </>
  );
}
```
Fix the state update so React re-renders correctly.


**Constraints:**
Do not mutate state directly.


**Prelims topic:**
immutable state updates, arrays in state.

---

#### 9. Reusable Button Component

**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Problem:**
Create a `Button` component that accepts `label`, `onClick`, and `color` props. Render a `<button>` whose text is `label`, whose click handler is `onClick`, and whose background uses the Tailwind color class passed in `color` (e.g., `"bg-blue-500"`). Use it inside `App` to render two different colored buttons.


**Example:**
```jsx
<Button label="Save" color="bg-blue-500" onClick={handleSave} />
```
renders a blue button with the text "Save".


**Constraints:**
- Use destructured props.
- Use `className` with the Tailwind class.


**Prelims topic:**
components, props, Tailwind in React.

---

#### 10. Multi-Input Registration Form

**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build a form with two inputs: `name` and `email`. Store both in a single state object `{name: '', email: ''}`. On submit, prevent the default form action and log the current state to the console.


**Example:**
Typing "Ana" in the name field and "ana@mail.com" in the email field, then pressing submit, logs `{name: "Ana", email: "ana@mail.com"}`.


**Constraints:**
- Use one `useState` object.
- Each input must update its own field in the object.


**Prelims topic:**
form state, controlled components, event handlers.

---

#### 11. Debug: Stale Closure with setCount

**Category:** React.js — **Difficulty:** Medium — **Type:** Debug

**Problem:**
Rapidly clicking the button only increments by the value that existed when the button was first clicked.
```jsx
function Counter() {
  const [count, setCount] = useState(0);
  const increment = () => setTimeout(() => setCount(count + 1), 1000);
  return <button onClick={increment}>+</button>;
}
```
Fix the update so it always uses the latest state.


**Constraints:**
Use the functional updater form of `setCount`.


**Prelims topic:**
`useState` updater, closures.

---

#### 12. Tab Switcher

**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build a `Tabs` component with tabs "Projects", "About", and "Contact". Only the content for the currently active tab is visible. Use `useState` to track the active tab and a function to switch between them.


**Example:**
Clicking the "About" tab shows the About section and hides the others.


**Constraints:**
- Use conditional rendering.
- Use a single state value for the active tab.


**Prelims topic:**
conditional rendering, state.

---

### Hard

#### 13. Shopping Cart

**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Problem:**
Build a `Cart` component with products `Apple` (₱15) and `Banana` (₱10). Display each product with minus/plus buttons, the current quantity, and a running total. Store quantities in a state object `{Apple: 1, Banana: 2}` and update it immutably.


**Example:**
Initial render shows:
```
Apple x1  +  -   ₱15
Banana x2  +  -   ₱20
Total: ₱35
```
Clicking `+` for Apple updates the quantity and total.


**Constraints:**
- State must be immutable.
- Total must be a derived value computed from state.


**Prelims topic:**
nested object state, derived state, event handlers.

---

#### 14. Debug: Missing List Keys

**Category:** React.js — **Difficulty:** Hard — **Type:** Debug

**Problem:**
When the list is reordered, React does not update correctly and a console warning appears.
```jsx
function List({ items }) {
  return <ul>{items.map(item => <li>{item}</li>)}</ul>;
}
```
Assume `items` is now an array of objects `{id, name}`. Add a reliable `key` and render the `name`.


**Constraints:**
`key` must be unique and stable across reorders.


**Prelims topic:**
list keys, component identity.

---

#### 15. Multi-Step Wizard

**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Problem:**
Build a 3-step form wizard:
- Step 1: ask for `name`.
- Step 2: ask for `course`.
- Step 3: show a summary with both values and a "Submit" button.

Include "Next" and "Back" buttons. Data must persist when moving between steps.


**Example:**
On step 2, clicking Back returns to step 1 with the name still filled.


**Constraints:**
Use one state object to hold all step data.


**Prelims topic:**
multi-step state, conditional rendering.

---

#### 16. Debug: Nested State Spread

**Category:** React.js — **Difficulty:** Hard — **Type:** Debug

**Problem:**
The UI does not update when the theme is toggled.
```jsx
const [user, setUser] = useState({ name: 'Ana', prefs: { theme: 'light' } });
const toggle = () => {
  user.prefs.theme = 'dark';
  setUser(user);
};
```
Fix the toggle so it updates the nested `theme` property immutably.


**Constraints:**
Do not mutate the existing `user` object or its `prefs` object.


**Prelims topic:**
nested state, immutability, object spread.

---

#### 17. Tailwind Card with Children

**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Problem:**
Create a reusable `Card` component that accepts `title`, `tech`, and `children` props. Render a white card with padding, rounded corners, and a shadow using Tailwind classes. Use `children` to render the card body. Use it in `App` to display two different project cards.


**Example:**
```jsx
<Card title="Weather App" tech="React">
  <p>A 5-day forecast app.</p>
</Card>
```


**Constraints:**
- Use `children`.
- Use `className` with Tailwind utilities such as `p-6 bg-white rounded-lg shadow`.


**Prelims topic:**
components, composition, Tailwind in React.

---

## CSS & Tailwind CSS

### Easy

#### 18. Debug: CSS Not Applied

**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Debug

**Problem:**
The external stylesheet `styles.css` is not being applied because of this tag:
```html
<head>
  <style>styles.css</style>
</head>
```
Fix it so the stylesheet loads correctly.


**Constraints:**
Use a `<link>` tag, not a `<style>` tag, for external CSS.


**Prelims topic:**
attaching external CSS.

---

#### 19. Basic Text Styles

**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a CSS rule for `body` that sets:
- `font-family` with fallbacks `'Calibri', Arial, sans-serif`
- `font-size: 16px`
- `line-height: 1.5`
- `color: #2B2D42`

Also write a `.muted` class that uses `#676C8A`.


**Example:**
```css
body {
  font-family: 'Calibri', Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #2B2D42;
}
.muted { color: #676C8A; }
```


**Constraints:**
Include font fallbacks.


**Prelims topic:**
text styling, color, units.

---

#### 20. Tailwind Card Utilities

**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Build

**Problem:**
Convert this CSS into a single Tailwind `className` string. Do not write custom CSS.
```css
.card {
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,.1);
}
```


**Example:**
```jsx
className="p-4 bg-white rounded-lg shadow"
```


**Constraints:**
Use only Tailwind utility classes.


**Prelims topic:**
Tailwind utility-first styling, spacing scale.

---

#### 21. Debug: Specificity Loses

**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Debug

**Problem:**
```html
<style>
  .title { color: navy; }
  #main-title { color: red; }
  h1 { color: green; }
</style>
<h1 id="main-title" class="title">Hello</h1>
```
What color will the heading be, and why? Then simplify the markup and CSS so the title is navy without using `!important` or an `id`.


**Constraints:**
Do not use `!important`.


**Prelims topic:**
specificity, selector types.

---

#### 22. Flexbox Centering

**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a `.hero` CSS class that makes its content perfectly centered both horizontally and vertically and takes the full viewport height.


**Example:**
```css
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
```


**Constraints:**
Use flexbox, not absolute positioning.


**Prelims topic:**
flexbox, `justify-content`, `align-items`, viewport units.

---

#### 23. Debug: Box Model Overflow

**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Debug

**Problem:**
```css
.box {
  width: 300px;
  padding: 20px;
  border: 2px solid black;
}
```
The rendered box is wider than 300px. Add one global rule so that `width: 300px` means the whole box including padding and border.


**Constraints:**
The rule should apply to all elements.


**Prelims topic:**
box model, `box-sizing`.

---

### Medium

#### 24. Responsive Nav Bar

**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build a responsive navigation bar with plain CSS. On mobile, the logo and links stack vertically. On desktop (`min-width: 768px`), they sit in a row with the logo on the left and the links on the right.


**Example:**
```css
.nav {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
@media (min-width: 768px) {
  .nav {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
```


**Constraints:**
- Mobile-first: write base styles for small screens, then add a media query.
- Use flexbox.


**Prelims topic:**
flexbox, media queries, responsive design.

---

#### 25. Debug: Tailwind `class` in JSX

**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Debug

**Problem:**
```jsx
function Card() {
  return <div class="p-4 bg-white rounded">Card</div>;
}
```
The Tailwind classes are not applied and a warning appears. Also, the rounded corners should be `rounded-lg` (8px). Fix both issues.


**Constraints:**
Use `className` in JSX. Use the correct Tailwind radius scale.


**Prelims topic:**
Tailwind in React, `className`.

---

#### 26. Responsive Card Gallery

**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Problem:**
Write a single Tailwind `className` for a card grid that has:
- 1 column on mobile
- 2 columns from `md:` (768px) up
- 3 columns from `lg:` (1024px) up
- a 24px gap


**Example:**
```jsx
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
```


**Constraints:**
No custom CSS. Use Tailwind responsive prefixes.


**Prelims topic:**
Tailwind grid, responsive breakpoints.

---

#### 27. Debug: Missing Viewport Meta

**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Debug

**Problem:**
```html
<head>
  <title>My App</title>
</head>
```
The site does not respond to media queries on a phone. Add the missing viewport meta tag.


**Constraints:**
Must be placed inside `<head>`.


**Prelims topic:**
viewport meta, responsive design.

---

#### 28. CSS Custom Properties Theme

**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Problem:**
Define `--brand` and `--accent` colors in `:root`. Write `.button` that uses `--brand` for the background and `.button:hover` that uses `--accent`.


**Example:**
```css
:root {
  --brand: #1A1B3A;
  --accent: #F08A24;
}
.button {
  background: var(--brand);
  padding: 16px;
}
.button:hover {
  background: var(--accent);
}
```


**Constraints:**
Use `var()` to read the variables.


**Prelims topic:**
CSS custom properties, hover states.

---

#### 29. Accessible Form Styling

**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Problem:**
Style a form with Tailwind. Each input should:
- have a visible focus ring
- have a label
- show grey helper text
The submit button should change background on hover.


**Example:**
```jsx
<input className="p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
<button className="px-4 py-2 bg-navy text-white hover:bg-orange">Submit</button>
```


**Constraints:**
- Use `focus:` classes.
- Ensure keyboard focus is visible.


**Prelims topic:**
Tailwind forms, hover/focus states, accessibility.

---

### Hard

#### 30. Full Landing Page with Tailwind

**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Build

**Problem:**
Build a complete landing page using **only** Tailwind utility classes. Include:
1. A `<nav>` with a logo on the left and links on the right.
2. A centered `<section>` hero with a heading, subtitle, and button.
3. A card grid of three project cards.
4. A `<footer>`.

Make it responsive: the card grid should be 1 column on mobile and 3 columns on desktop.

**Example class choices:**
- Nav: `flex justify-between items-center p-4`
- Hero: `h-screen flex flex-col justify-center items-center text-center`
- Cards: `grid grid-cols-1 md:grid-cols-3 gap-6`


**Constraints:**
No custom CSS in a `.css` file.


**Prelims topic:**
Tailwind in practice, responsive layout, flex/grid.

---

#### 31. Debug: Bootstrap vs Tailwind Conflict

**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Debug

**Problem:**
An HTML page loads Bootstrap CSS and then Tailwind CSS. A button has both classes:
```html
<button class="btn btn-primary px-4 py-2 bg-blue-500 text-white rounded">
  Save
</button>
```
The button looks broken because Bootstrap and Tailwind fight. Remove the Bootstrap classes and rewrite the button using only Tailwind utilities.


**Constraints:**
No Bootstrap classes. Use Tailwind utilities for all styling.


**Prelims topic:**
Tailwind utility-first, avoiding framework conflicts.

---

#### 32. Dashboard Layout

**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Build

**Problem:**
Build a dashboard layout using CSS Grid. On desktop, show a 250px sidebar on the left and a main content area on the right. On mobile, hide the sidebar and make the main area full width.


**Example:**
```css
.layout {
  display: grid;
  grid-template-columns: 1fr;
}
@media (min-width: 768px) {
  .layout {
    grid-template-columns: 250px 1fr;
  }
}
```


**Constraints:**
- Use `grid-template-columns`.
- Use a media query.
- Do not use a framework.


**Prelims topic:**
CSS Grid, responsive design, layout.

---

#### 33. Debug: Specificity War

**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Debug

**Problem:**
A stylesheet is full of selectors like `#header #nav a` and `#main #nav a` and uses `!important` for colors. Link colors are inconsistent and hard to override. Refactor the nav to use simple class selectors and remove `!important`.


**Constraints:**
- No `!important`.
- No `id` selectors in the nav styles.


**Prelims topic:**
specificity, selector simplification.

---

#### 34. Convert Plain CSS to Tailwind

**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Build

**Problem:**
You are given this CSS for a card, button, and grid:
```css
.card { padding: 24px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,.1); }
.btn { padding: 8px 16px; background: navy; color: white; border-radius: 8px; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
```
Convert it to Tailwind utility classes in JSX. For each original CSS rule, write the equivalent Tailwind `className` string.

**Example mapping:**
- `.card` → `p-6 bg-white rounded-lg shadow`
- `.btn` → `px-4 py-2 bg-navy text-white rounded-lg`
- `.grid` → `grid grid-cols-3 gap-6`


**Constraints:**
No custom CSS classes. Use only Tailwind utilities.


**Prelims topic:**
CSS to Tailwind mapping, utility-first.

---

## Python & FastAPI

### Easy

#### 35. FastAPI Hello World

**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Problem:**
Create a `main.py` file with a FastAPI app. Add a `GET /` route that returns the JSON object `{"message": "Hello from the server"}`.


**Example:**
When you visit `http://127.0.0.1:8000/`, the browser shows:
```json
{ "message": "Hello from the server" }
```


**Constraints:**
- Use `FastAPI()`.
- Use the `@app.get("/")` decorator.


**Prelims topic:**
FastAPI first app, route decorator.

---

#### 36. Debug: Python Indentation

**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Debug

**Problem:**
```python
def greet(name):
if name == "Ana":
    return f"Hello, {name}"
return "Hello, stranger"
```
This function raises an `IndentationError`. Fix the indentation.


**Constraints:**
Use 4 spaces consistently.


**Prelims topic:**
Python syntax, indentation.

---

#### 37. Student Info in Python

**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a function `describe(student)` that takes a dict `{"name": "Ana", "year": 3}` and returns the f-string `"Ana is in year 3"`. Also write a function `total(prices)` that returns the sum of a list of numbers.


**Example:**
```python
describe({"name": "Ana", "year": 3})  # "Ana is in year 3"
total([90, 75, 88])                   # 253
```


**Constraints:**
- Use f-strings.
- Use the built-in `sum()`.


**Prelims topic:**
Python dict/list, f-strings, functions.

---

#### 38. GET /projects List

**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Problem:**
Create a FastAPI `GET /projects` route that returns a list of exactly two project dictionaries. Each project must have `id`, `title`, and `tech`.


**Example:**
```json
[
  { "id": 1, "title": "Weather App", "tech": "React" },
  { "id": 2, "title": "Inventory", "tech": "FastAPI" }
]
```


**Constraints:**
- Use a Python list of dicts.
- Use a plural noun for the route path.


**Prelims topic:**
FastAPI routes, GET, JSON response.

---

#### 39. Path Parameter Route

**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Problem:**
Add a `GET /projects/{project_id}` route. The path parameter must be typed as `int`. The route returns:
```json
{ "id": project_id, "title": "Weather App" }
```


**Example:**
A request to `GET /projects/5` returns:
```json
{ "id": 5, "title": "Weather App" }
```


**Constraints:**
`project_id` must have type hint `int`.


**Prelims topic:**
path parameters, type hints.

---

### Medium

#### 40. Debug: Create Returns 200 Not 201

**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Debug

**Problem:**
```python
@app.post("/projects")
def create_project(project: Project):
    new_project = { "id": 1, "title": project.title }
    return new_project
```
A successful create should return HTTP 201. Fix the route decorator.


**Constraints:**
Do not return `200` for a creation endpoint.


**Prelims topic:**
HTTP status codes, POST.

---

#### 41. POST with Pydantic

**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Build

**Problem:**
Define a Pydantic model `Project` with `title: str`, `tech: str`, and an optional `stars: int = 0`. Create a `POST /projects` route that accepts a `Project` body and returns:
```json
{ "created": project.title, "tech": project.tech, "stars": project.stars }
```


**Example:**
`POST /projects` with body `{"title":"X","tech":"Y"}` returns:
```json
{ "created": "X", "tech": "Y", "stars": 0 }
```


**Constraints:**
- Inherit from `BaseModel`.
- `stars` must have a default value.


**Prelims topic:**
Pydantic, request body, POST.

---

#### 42. Query Parameters

**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Build

**Problem:**
Add a `GET /projects` route with query parameters `tech: str = "all"` and `limit: int = 10`. It should return projects filtered by `tech` (case-insensitive), limited to `limit` results.


**Example:**
Given projects `Weather App (React)`, `Inventory (FastAPI)`, `Portfolio (React)`:
- `GET /projects?tech=react&limit=2` returns the first 2 React projects.
- `GET /projects` returns all projects.


**Constraints:**
- Query params must have defaults.
- Filtering must be case-insensitive.


**Prelims topic:**
query parameters, defaults, filtering.

---

#### 43. Debug: 404 as Normal Body

**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Debug

**Problem:**
```python
@app.get("/projects/{project_id}")
def get_project(project_id: int):
    if project_id != 1:
        return { "error": "Project not found" }
    return { "id": 1, "title": "Weather App" }
```
A missing project should return HTTP 404, not a 200 response with an error body. Fix it.


**Constraints:**
Use `HTTPException`.


**Prelims topic:**
HTTP status codes, error handling.

---

#### 44. In-Memory CRUD API

**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build a full in-memory CRUD API for `projects`:
- `GET /projects` — list all
- `GET /projects/{project_id}` — get one or 404
- `POST /projects` — create with status 201
- `DELETE /projects/{project_id}` — delete or 404

Use a Pydantic model for creation. Store data in a global Python list.


**Example:**
After `POST /projects {"title":"X","tech":"Y"}`, `GET /projects` includes the new item. After `DELETE /projects/1`, it is gone.


**Constraints:**
- Use proper status codes (`201`, `404`).
- IDs should be unique and auto-incrementing.


**Prelims topic:**
CRUD, REST, FastAPI, HTTP methods.

---

### Hard

#### 45. Nested Pydantic Body

**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Problem:**
Define two Pydantic models:
- `Skill` with `name: str` and `level: int` (must be ≥ 1)
- `Project` with `title: str`, `tech: str`, and `skills: list[Skill]`

Create a `POST /projects` route that validates the nested body and returns the project as JSON.


**Example:**
```json
POST /projects
{
  "title": "Weather App",
  "tech": "React",
  "skills": [
    { "name": "React", "level": 3 }
  ]
}
```


**Constraints:**
- Use nested `BaseModel`.
- Validate `level` is a positive integer.


**Prelims topic:**
Pydantic, nested models, validation.

---

#### 46. Debug: Type Hint Rejection

**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Debug

**Problem:**
```python
@app.get("/projects/{project_id}")
def get_project(project_id: int):
    return { "id": project_id }
```
A request to `GET /projects/abc` currently causes a 500 server error. FastAPI should automatically reject it with a clear validation error.

What status code and body should FastAPI return, and why? Explain the fix (no code change is necessary if the route is written correctly).


**Constraints:**
Let FastAPI's type hints do the validation.


**Prelims topic:**
type hints, validation, status 422.

---

#### 47. Complete FastAPI App with Docs

**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Problem:**
Build a FastAPI app with these routes:
- `GET /` — returns a welcome message
- `GET /projects` — returns a list of two project dicts
- `GET /about` — returns your name and course

Run the app and test all three routes from the automatic `/docs` page.


**Example:**
- `GET /` → `{"message":"Projects API"}`
- `GET /projects` → `[{...}, {...}]`
- `GET /about` → `{"name":"Ana","course":"BSCS"}`


**Constraints:**
- Use noun paths, not verbs (e.g., `/projects`, not `/getProjects`).
- Test through `http://127.0.0.1:8000/docs`.


**Prelims topic:**
FastAPI routes, interactive docs, REST naming.

---

#### 48. Group and Sort Projects

**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Problem:**
Write a Python function `group_by_tech(projects)` that takes a list of dicts with `title` and `tech` and returns a dict mapping each `tech` to a sorted list of titles.


**Example:**
```python
group_by_tech([
  { "title": "Weather", "tech": "React" },
  { "title": "Inventory", "tech": "FastAPI" },
  { "title": "Portfolio", "tech": "React" }
])
# returns { "React": ["Portfolio", "Weather"], "FastAPI": ["Inventory"] }
```


**Constraints:**
- Sort each tech's list alphabetically.
- Return a plain Python dict.


**Prelims topic:**
Python dict/list manipulation, grouping.

---

#### 49. Debug: Broken DELETE and POST ID

**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Debug

**Problem:**
```python
@app.post("/projects", status_code=201)
def create_project(project: Project):
    new = { "id": len(projects), "title": project.title, "tech": project.tech }
    projects.append(new)
    return new

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    for i, p in enumerate(projects):
        if p["id"] == project_id:
            projects.pop(i)
```

There are two bugs:
1. New project IDs start at `0` and can collide with existing IDs.
2. The `DELETE` route silently fails when the project does not exist.

Fix both.


**Constraints:**
IDs must be unique. DELETE must return 404 on missing.


**Prelims topic:**
CRUD, status codes, list operations.

---

#### 50. Full FastAPI App with Validation and Errors

**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Problem:**
Build a complete FastAPI `projects` API with:
- Pydantic model for project creation
- `GET /projects`, `GET /projects/{id}`, `POST /projects`, `DELETE /projects/{id}`
- Path and query parameters
- `404` errors for missing items
- `201` status for creation
- A `GET /health` route returning `{"status": "ok"}`

Test it using `/docs`.


**Example:**
- `GET /health` → `{"status":"ok"}`
- `POST /projects {"title":"X","tech":"Y"}` → 201 + new project
- `GET /projects/999` → 404


**Constraints:**
- Use Pydantic, `HTTPException`, `status_code`, and type hints.
- Data is stored in memory.


**Prelims topic:**
full FastAPI app, validation, status codes, docs.

---

## HTML, Accessibility & Deployment

### Easy

#### 51. Semantic Portfolio Skeleton

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a complete, valid HTML5 page skeleton for a portfolio. The page must include:
- `<!DOCTYPE html>`, `<html lang="en">`, `<head>` with `charset="UTF-8"` and the viewport meta tag.
- A `<title>` that is not blank.
- A `<body>` with `<header>`, `<nav>` (containing two links), `<main>` with two `<section>` elements, and `<footer>`.


**Example output:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Portfolio</title>
</head>
<body>
  <header>
    <h1>My Portfolio</h1>
    <nav><a href="#about">About</a> <a href="#work">Work</a></nav>
  </header>
  <main>
    <section id="about">About me.</section>
    <section id="work">My work.</section>
  </main>
  <footer>&copy; 2026</footer>
</body>
</html>
```


**Constraints:**
- Do not use `<div>` where a semantic element exists.
- There must be exactly one `<h1>` and one `<main>`.


**Prelims topic:**
Semantic HTML5, document structure, landmarks.

---

#### 52. Debug: Div Soup to Semantic

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Easy — **Type:** Debug

**Problem:**
A teammate wrote this non-semantic markup:
```html
<div class="header">
  <div class="logo">My Site</div>
  <div class="menu"><a href="/">Home</a></div>
</div>
<div class="main">
  <div class="post">...</div>
</div>
<div class="footer">...</div>
```
Rewrite it using semantic HTML5 elements.


**Constraints:**
- Use `<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`.
- Do not keep the class-named `<div>` for structure.


**Prelims topic:**
Semantic elements, div misuse.

---

#### 53. Debug: Broken Heading Hierarchy

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Easy — **Type:** Debug

**Problem:**
This heading outline is broken:
```html
<h1>My Portfolio</h1>
<h4>About Me</h4>
<h2>Projects</h2>
<h4>Contact</h4>
```
Fix the hierarchy so levels are not skipped. Keep the same page structure and change the size with CSS, not the tag.


**Constraints:**
- One `<h1>` per page.
- Do not skip heading levels (`h2` follows `h1`).


**Prelims topic:**
Heading hierarchy, document outline.

---

#### 54. Build: Article with Figure

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a self-contained `<article>` that represents a project. It must include:
- A heading.
- A `<figure>` containing an `<img>` with descriptive `alt` text and a `<figcaption>`.


**Example output:**
```html
<article>
  <h2>Weather App</h2>
  <figure>
    <img src="weather.png" alt="Weather dashboard showing a five-day forecast for Manila">
    <figcaption>Weather App screenshot</figcaption>
  </figure>
</article>
```


**Constraints:**
- Use `<article>`, `<figure>`, `<img>`, and `<figcaption>`.
- The `alt` text must describe the image's purpose, not its filename.


**Prelims topic:**
article, figure, figcaption, alt text.

---

#### 55. Debug: Missing Lang and Viewport

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Easy — **Type:** Debug

**Problem:**
This page head is missing two important things:
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Portfolio</title>
</head>
```
Add the missing attributes and meta tag that help accessibility and responsiveness.


**Constraints:**
- Add `lang="en"` to `<html>`.
- Add the viewport `<meta>` in the `<head>`.


**Prelims topic:**
lang attribute, viewport meta, responsive design, screen readers.

---


### Medium

#### 56. Build: Accessible Contact Form

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build an accessible contact form with fields for Name, Email, and Message. The form must be usable by keyboard and screen-reader users.


**Example output:**
```html
<form>
  <label for="name">Name</label>
  <input type="text" id="name" name="name">

  <label for="email">Email</label>
  <input type="email" id="email" name="email">

  <label for="message">Message</label>
  <textarea id="message" name="message"></textarea>

  <p class="error">Error: email is required.</p>
  <button type="submit">Send</button>
</form>
```


**Constraints:**
- Every input must have a `<label>` with matching `for`/`id`.
- Do not use placeholders as the only label.
- Error text must start with the word "Error" and not rely on colour alone.
- The submit button must be focusable and triggerable with Enter.


**Prelims topic:**
Form accessibility, labels, placeholders, colour not alone, keyboard access.

---

#### 57. Debug: Bad Alt Text and Missing Labels

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Medium — **Type:** Debug

**Problem:**
This markup has three accessibility problems:
```html
<img src="p1.png" alt="p1.png">
<input type="text" placeholder="Email">
<p style="color:red">Invalid</p>
```
Fix all three.


**Constraints:**
- `alt` must describe the image's purpose.
- Use `<label for="...">` that matches the input `id`.
- Error message must not rely on colour alone.


**Prelims topic:**
Alt text, labels, error messages, colour not alone.

---

#### 58. Build: Accessible Landing Page

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build a one-page portfolio landing page that is fully accessible. It should include:
- Semantic landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`.
- A "Skip to main content" link.
- One `<h1>` and a logical heading hierarchy.
- Alt text on every image.
- Linked labels on any form controls.
- Visible focus styles for keyboard users.


**Example output:**
A single HTML file with the structure above.


**Constraints:**
- No `<div>` where a semantic element can be used.
- Include a `href="#main"` skip link and `<main id="main">`.
- All form inputs must have labels.


**Prelims topic:**
Landmarks, skip links, heading hierarchy, alt text, labels, keyboard focus.

---


### Hard

#### 59. Deployment: Push-to-Publish Pipeline

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Hard — **Type:** Build

**Problem:**
Explain, step by step, how a static site goes from a local folder on your laptop to a public URL. Also explain why a FastAPI back end cannot be served by a pure static host such as Netlify or Cloudflare Pages.


**Constraints:**
- Include `git commit`, `git push`, host connection, and automatic rebuild.
- Distinguish between serving files and running code.


**Prelims topic:**
Deployment, static hosting, Git, FastAPI difference.

---

#### 60. Debug: Broken Images on Live Site

**Category:** HTML, Accessibility & Deployment — **Difficulty:** Hard — **Type:** Debug

**Problem:**
Your site looks fine when you open it from your laptop, but images are broken on the live site. What is the most likely cause, and what is your checklist to fix and prevent it?


**Constraints:**
- Mention case sensitivity and repository paths.
- Include at least three actionable checks.


**Prelims topic:**
Deployment, file paths, static hosting, Git.

---


---

## React.js

### Easy

#### 61. Debug: Self-Closing Tags in JSX

**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Problem:**
This JSX fails to compile because three tags are not self-closed:
```jsx
function App() {
  return (
    <div>
      <img src="logo.png">
      <br>
      <input type="text">
    </div>
  );
}
```
Fix it.


**Constraints:**
- Every JSX tag must close: `<img />`, `<br />`, `<input />`.


**Prelims topic:**
JSX, self-closing tags.

---

#### 62. Build: Greeting Card with Props

**Category:** React.js — **Difficulty:** Easy — **Type:** Build

**Problem:**
Write a `Card` component that receives `name` and `role` props and renders them. Then render a list of cards from an array of people.


**Example:**
```jsx
const people = [
  { id: 1, name: "Ana", role: "Student" },
  { id: 2, name: "Ben", role: "Tutor" }
];

// Render:
// <Card name="Ana" role="Student" />
// <Card name="Ben" role="Tutor" />
```


**Constraints:**
- Component name must start with a capital letter.
- Use props.
- Use `people.map(...)` and a stable `key` from the data.


**Prelims topic:**
Components, JSX, props, map, keys.

---

#### 63. Debug: Lowercase Component Name

**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Problem:**
This component does not render as a custom component:
```jsx
function profileCard({ name }) {
  return <h2>{name}</h2>;
}

function App() {
  return <profileCard name="Ana" />;
}
```
Fix it.


**Constraints:**
- Rename the function to start with a capital letter.
- Update the JSX tag to match.


**Prelims topic:**
Component naming, JSX.

---


### Medium

#### 64. Debug: Missing Curly Braces in JSX

**Category:** React.js — **Difficulty:** Medium — **Type:** Debug

**Problem:**
This component renders the literal word "name" instead of the variable:
```jsx
function Greeting() {
  const name = "Ana";
  return <p>Hello, name</p>;
}
```
Fix it.


**Constraints:**
- Use curly braces `{}` for JavaScript expressions inside JSX.


**Prelims topic:**
JSX, curly braces, JavaScript expressions.

---

#### 65. Build: Project List with Props and Keys

**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Problem:**
Write a `Project` component that takes `title`, `tech`, and `link` props and renders a card with a link. In `App`, map over the `projects` array and render one `Project` for each item, using a stable key.


**Example:**
```jsx
const projects = [
  { id: 1, title: "Weather App", tech: "React", link: "..." },
  { id: 2, title: "Inventory", tech: "FastAPI", link: "..." }
];

// Renders two Project cards.
```


**Constraints:**
- Use a real `id` from the data as the `key`, not the array index.
- Pass all three props.
- The component name is capitalised.


**Prelims topic:**
Components, props, map, keys, composition.

---

#### 66. Debug: Mutating Props Directly

**Category:** React.js — **Difficulty:** Medium — **Type:** Debug

**Problem:**
This component tries to change a prop, which is not allowed:
```jsx
function Greeting({ name }) {
  name = name.toUpperCase();
  return <h1>{name}</h1>;
}
```
Fix it without creating state. Use a derived value in the render.


**Constraints:**
- Props are read-only. Do not reassign them.
- Compute the final value during render.


**Prelims topic:**
Props, read-only, derived values.

---

#### 67. Build: Controlled Name Input

**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Problem:**
Build a `NameBox` component with `useState`. It should have an input and a paragraph that shows `Hello, {name}` as the user types.


**Example:**
Typing "Ana" shows:
```jsx
<p>Hello, Ana</p>
```


**Constraints:**
- Use `useState` for the name.
- Bind the input's `value` to state.
- Use `onChange` with `e.target.value` to update state.
- Pass the function, do not call it.


**Prelims topic:**
State, useState, events, controlled inputs.

---


### Hard

#### 68. Build: Toggle Contact Details

**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Problem:**
Build an `App` with a button that toggles the visibility of a contact details section. Use `useState` and conditional rendering.


**Example:**
- Initially, only the button "Show contact" is visible.
- Clicking the button shows the email and changes the label to "Hide contact".
- Clicking again hides it.


**Constraints:**
- Use `useState` for the toggle state.
- `onClick` must pass the setter function, not call it (`setShow(!show)`).
- Conditionally render the contact section.


**Prelims topic:**
State, events, conditional rendering.

---

#### 69. Build: Week 2 Portfolio in React

**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Problem:**
Rebuild the Week 2 portfolio as React components. The app must include:
- A `Header` component that shows your name.
- A reusable `ProjectCard` component used with different props.
- A list of projects rendered with `map` and a stable `key`.
- A button that toggles contact details with `useState`.


**Example:**
A page with a header, three project cards, and a "Show contact" button that reveals an email.


**Constraints:**
- At least two components.
- Use props.
- Use `map` with a real `id` as `key`.
- Use `useState` and an event handler.
- Do not touch the DOM manually.


**Prelims topic:**
Components, props, state, events, composition, Vite app structure.

---

#### 70. Debug: Index as Key in Sortable List

**Category:** React.js — **Difficulty:** Hard — **Type:** Debug

**Problem:**
This list uses the array index as the key. It causes subtle bugs when the list is reordered or filtered:
```jsx
<ul>
  {projects.map((p, index) => (
    <li key={index}>{p.title}</li>
  ))}
</ul>
```
Rewrite it to use a stable key and explain why the index is risky.


**Constraints:**
- Use `p.id` (a stable value from the data) as the key.
- Explain the bug in a comment or short paragraph.


**Prelims topic:**
Keys, list rendering, reconciliation.
