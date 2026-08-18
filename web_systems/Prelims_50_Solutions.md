# Prelims 50 Solutions
Reference answers / expected fixes for the original problem set.

## 1. Counter Component
**Category:** React.js — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
After 3 clicks, the page should display:
```
You have clicked the button 3 times.
```

## 2. Debug: Class vs className
**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Expected fix:**
```jsx
<h1 className="title text-navy">Hello</h1>
```

## 3. Fruit List with Keys
**Category:** React.js — **Difficulty:** Easy — **Type:** Build

**Reference Example output:**
```html
<ul>
  <li>Apple</li>
  <li>Banana</li>
  <li>Orange</li>
</ul>
```

## 4. Debug: Adjacent JSX Elements
**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Expected fix:**
```jsx
export default function App() {
  return (
    <>
      <h1>Title</h1>
      <p>Subtitle</p>
    </>
  );
}
```

## 5. Dynamic Title
**Category:** React.js — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
If `title = "My React App"`, the page shows an `<h1>` and a `<p>` both containing that title.

## 6. Debug: onClick Called Immediately
**Category:** React.js — **Difficulty:** Easy — **Type:** Debug

**Expected fix:**
```jsx
<button onClick={() => setCount(count + 1)}>Click</button>
```

## 7. Filterable Project List
**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
Given `[{id:1, title:"Weather App", tech:"React"}, {id:2, title:"Inventory", tech:"FastAPI"}]` and the search term `"React"`, only the Weather App card is shown.

## 8. Debug: Mutating State Array
**Category:** React.js — **Difficulty:** Medium — **Type:** Debug

**Expected fix:**
```js
const add = () => setTodos([...todos, 'Walk dog']);
```

## 9. Reusable Button Component
**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
```jsx
<Button label="Save" color="bg-blue-500" onClick={handleSave} />
```
renders a blue button with the text "Save".

## 10. Multi-Input Registration Form
**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
Typing "Ana" in the name field and "ana@mail.com" in the email field, then pressing submit, logs `{name: "Ana", email: "ana@mail.com"}`.

## 11. Debug: Stale Closure with setCount
**Category:** React.js — **Difficulty:** Medium — **Type:** Debug

**Expected fix:**
```js
setTimeout(() => setCount(c => c + 1), 1000)
```

## 12. Tab Switcher
**Category:** React.js — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
Clicking the "About" tab shows the About section and hides the others.

## 13. Shopping Cart
**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
Initial render shows:
```
Apple x1  +  -   ₱15
Banana x2  +  -   ₱20
Total: ₱35
```
Clicking `+` for Apple updates the quantity and total.

## 14. Debug: Missing List Keys
**Category:** React.js — **Difficulty:** Hard — **Type:** Debug

**Expected fix:**
```jsx
<ul>{items.map(item => <li key={item.id}>{item.name}</li>)}</ul>
```

## 15. Multi-Step Wizard
**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
On step 2, clicking Back returns to step 1 with the name still filled.

## 16. Debug: Nested State Spread
**Category:** React.js — **Difficulty:** Hard — **Type:** Debug

**Expected fix:**
```js
setUser({ ...user, prefs: { ...user.prefs, theme: 'dark' } });
```

## 17. Tailwind Card with Children
**Category:** React.js — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
```jsx
<Card title="Weather App" tech="React">
  <p>A 5-day forecast app.</p>
</Card>
```

## 18. Debug: CSS Not Applied
**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Debug

**Expected fix:**
```html
<link rel="stylesheet" href="styles.css">
```

## 19. Basic Text Styles
**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
```css
body {
  font-family: 'Calibri', Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #2B2D42;
}
.muted { color: #676C8A; }
```

## 20. Tailwind Card Utilities
**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
```jsx
className="p-4 bg-white rounded-lg shadow"
```

## 21. Debug: Specificity Loses
**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Debug

**Expected answer:**
The heading is red because the `id` selector has the highest specificity. Simplified: `<h1 class="title">Hello</h1>` with `.title { color: navy; }`.

## 22. Flexbox Centering
**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
```css
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
```

## 23. Debug: Box Model Overflow
**Category:** CSS & Tailwind — **Difficulty:** Easy — **Type:** Debug

**Expected fix:**
```css
* {
  box-sizing: border-box;
}
```

## 24. Responsive Nav Bar
**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
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

## 25. Debug: Tailwind `class` in JSX
**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Debug

**Expected fix:**
```jsx
<div className="p-4 bg-white rounded-lg">Card</div>
```

## 26. Responsive Card Gallery
**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
```jsx
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
```

## 27. Debug: Missing Viewport Meta
**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Debug

**Expected fix:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

## 28. CSS Custom Properties Theme
**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
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

## 29. Accessible Form Styling
**Category:** CSS & Tailwind — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
```jsx
<input className="p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
<button className="px-4 py-2 bg-navy text-white hover:bg-orange">Submit</button>
```

## 30. Full Landing Page with Tailwind
**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Build

No fixed expected answer. Build an implementation that satisfies the problem statement and constraints.
## 31. Debug: Bootstrap vs Tailwind Conflict
**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Debug

**Expected fix:**
```html
<button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
  Save
</button>
```

## 32. Dashboard Layout
**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
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

## 33. Debug: Specificity War
**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Debug

**Expected approach:**
```css
.nav-link { color: navy; }
.nav-link:hover { color: orange; }
```

## 34. Convert Plain CSS to Tailwind
**Category:** CSS & Tailwind — **Difficulty:** Hard — **Type:** Build

No fixed expected answer. Build an implementation that satisfies the problem statement and constraints.
## 35. FastAPI Hello World
**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
When you visit `http://127.0.0.1:8000/`, the browser shows:
```json
{ "message": "Hello from the server" }
```

## 36. Debug: Python Indentation
**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Debug

**Expected fix:**
```python
def greet(name):
    if name == "Ana":
        return f"Hello, {name}"
    return "Hello, stranger"
```

## 37. Student Info in Python
**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
```python
describe({"name": "Ana", "year": 3})  # "Ana is in year 3"
total([90, 75, 88])                   # 253
```

## 38. GET /projects List
**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
```json
[
  { "id": 1, "title": "Weather App", "tech": "React" },
  { "id": 2, "title": "Inventory", "tech": "FastAPI" }
]
```

## 39. Path Parameter Route
**Category:** Python & FastAPI — **Difficulty:** Easy — **Type:** Build

**Reference Example:**
A request to `GET /projects/5` returns:
```json
{ "id": 5, "title": "Weather App" }
```

## 40. Debug: Create Returns 200 Not 201
**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Debug

**Expected fix:**
```python
@app.post("/projects", status_code=201)
```

## 41. POST with Pydantic
**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
`POST /projects` with body `{"title":"X","tech":"Y"}` returns:
```json
{ "created": "X", "tech": "Y", "stars": 0 }
```

## 42. Query Parameters
**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
Given projects `Weather App (React)`, `Inventory (FastAPI)`, `Portfolio (React)`:
- `GET /projects?tech=react&limit=2` returns the first 2 React projects.
- `GET /projects` returns all projects.

## 43. Debug: 404 as Normal Body
**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Debug

**Expected fix:**
```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Project not found")
```

## 44. In-Memory CRUD API
**Category:** Python & FastAPI — **Difficulty:** Medium — **Type:** Build

**Reference Example:**
After `POST /projects {"title":"X","tech":"Y"}`, `GET /projects` includes the new item. After `DELETE /projects/1`, it is gone.

## 45. Nested Pydantic Body
**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
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

## 46. Debug: Type Hint Rejection
**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Debug

**Expected answer:**
FastAPI returns `422 Unprocessable Entity` with a validation error because `project_id` is typed as `int`. The 500 error implies something else is wrong (e.g., manual conversion before the route). Remove any manual string-to-int parsing and let FastAPI validate the parameter.

## 47. Complete FastAPI App with Docs
**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
- `GET /` → `{"message":"Projects API"}`
- `GET /projects` → `[{...}, {...}]`
- `GET /about` → `{"name":"Ana","course":"BSCS"}`

## 48. Group and Sort Projects
**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
```python
group_by_tech([
  { "title": "Weather", "tech": "React" },
  { "title": "Inventory", "tech": "FastAPI" },
  { "title": "Portfolio", "tech": "React" }
])
# returns { "React": ["Portfolio", "Weather"], "FastAPI": ["Inventory"] }
```

## 49. Debug: Broken DELETE and POST ID
**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Debug

**Expected fix:**
- Use `len(projects) + 1` (or a running counter) for the new `id`.
- Raise `HTTPException(404, ...)` in `DELETE` if no project matches.

## 50. Full FastAPI App with Validation and Errors
**Category:** Python & FastAPI — **Difficulty:** Hard — **Type:** Build

**Reference Example:**
- `GET /health` → `{"status":"ok"}`
- `POST /projects {"title":"X","tech":"Y"}` → 201 + new project
- `GET /projects/999` → 404
