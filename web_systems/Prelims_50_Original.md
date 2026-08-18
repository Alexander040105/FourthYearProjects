# 50 Original Prelims Problems (Roulette Edition)

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
