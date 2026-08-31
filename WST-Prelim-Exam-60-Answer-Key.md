# WST 60-Item Prelim Exam (Answer Key)

**Instructions:** Answer key for the 60-item exam. Part I: 30 multiple-choice questions. Part II: 30 practical questions. Use this after answering the question sheet.

---

## Part I — Multiple Choice (2 points each)

| # | Difficulty | Question | A | B | C | D | Ans | Why |
|---|-----------|----------|---|---|---|---|---|-----|
| 1 | Easy | Two pages look the same; one uses `div`, the other uses semantic elements. Who can tell the difference? | Only the browser | Only developers reading the source | Screen readers, search engines and other developers | Nobody | C | Semantic markup has the same visual rendering but different meaning for assistive tech, search engines, and code readers. |
| 2 | Easy | What does a static host actually do? | Runs Python code for free | Serves files as-is | Validates forms server-side | Compiles React | B | Static hosts only copy and serve files; they cannot execute back-end code. |
| 3 | Easy | Which line in the `<head>` makes responsive CSS work on phones? | `<meta charset="UTF-8">` | `<meta name="viewport" content="width=device-width, initial-scale=1.0">` | `<link rel="stylesheet" href="styles.css">` | `<title>Portfolio</title>` | B | The viewport meta tag stops phones from rendering the page as a scaled desktop layout. |
| 4 | Medium | Why is it wrong to change an `<h2>` to `<h4>` just to make the text smaller? | It makes the page load slower | It breaks the document outline to fix a styling problem | It improves accessibility by adding hierarchy | It makes the text inaccessible | B | Heading levels are rank, not font size; use CSS to change size. |
| 5 | Easy | A decorative background image is an `<img>`. What should its `alt` be? | A full description of the flourish | The filename | `alt=""` | Omit the `alt` attribute | C | Decorative images should have an empty `alt` so screen readers skip them. |
| 6 | Easy | A form uses only `placeholder="Email"` instead of a `<label>`. What is the main problem? | It is harder to style | The hint disappears when the user types and may not be announced | The form will not submit | It takes too much space | B | Placeholders are not a substitute for labels. |
| 7 | Medium | Why can't the browser connect directly to the database? | It would require sending DB credentials to the user | Browsers cannot make network requests | HTML does not support databases | It is too slow | A | The back end holds credentials and enforces rules; exposing them would bypass security. |
| 8 | Medium | What does it mean that HTTP is stateless? | It is always encrypted | Each request is independent unless something extra carries identity | The server forgets everything automatically | Cookies are not allowed | B | HTTP does not remember the previous request; sessions/cookies/tokens add state. |
| 9 | Easy | What happens right after you run `git add .`? | Changes are committed | Changes are pushed to GitHub | Changes are staged for the next commit | Changes are deleted | C | `git add` only stages; `git commit` makes the snapshot. |
| 10 | Medium | Two functions each multiply a total by `1.12` to add VAT. Which principle is violated? | YAGNI | DRY | SOLID | KISS | B | Repeating the same logic in multiple places violates DRY. |
| 11 | Medium | You build tags, comments and a draft workflow that were not requested. Which principle is this? | DRY | SOLID | YAGNI | OOP | C | Building features that were not asked for violates YAGNI. |
| 12 | Medium | A single class validates input, hashes passwords, saves users and sends email. Which SOLID letter is broken? | S — Single Responsibility | O — Open/Closed | L — Liskov | D — Dependency Inversion | A | The class has more than one reason to change, violating S. |
| 13 | Hard | A route handler calls `psycopg.connect()` directly inside the function. What is the main cost? | It makes the code harder to read | It hard-wires the code to one database and makes testing difficult | It violates the Open/Closed principle | It leaks secrets into the front end | B | Directly instantiating a concrete dependency violates Dependency Inversion and prevents testing without a real DB. |
| 14 | Easy | Which of these should be in `.gitignore`? | `main.py` | `README.md` | `.venv/` | `requirements.txt` | C | `.venv/` is local and generated; it should not be committed. |
| 15 | Medium | Which selector wins over `.lead` regardless of source order? | `p { }` | `.lead { }` | `#intro { }` | `*` | C | ID selectors have higher specificity than class selectors. |
| 16 | Medium | What does `box-sizing: border-box` do? | Adds a visible border | Includes padding and border in the declared width | Removes margins | Forces a square box | B | It makes the `width` value refer to the total box size, not just content. |
| 17 | Medium | A paragraph has `margin-bottom: 20px` and the next has `margin-top: 20px`. What is the gap between them? | 40px | 20px | 0px | 30px | B | Vertical margins collapse to the larger single value. |
| 18 | Easy | In Tailwind, `p-4` is equivalent to which padding? | 4px | 8px | 16px | 32px | C | Tailwind's scale is 1 step = 4px, so `p-4` is 16px. |
| 19 | Medium | In Tailwind's mobile-first model, an unprefixed utility class applies... | only on desktop | at 0px and above unless a breakpoint overrides it | only on phones | inside media queries only | B | Mobile-first means the base class is for the smallest screen; `md:`/ `lg:` add rules for larger screens. |
| 20 | Easy | Why must a React component name start with a capital letter? | It is a style rule | React uses capitalization to tell components from HTML tags | Faster rendering | Required by Babel | B | `Welcome` is a component; `welcome` is treated as a normal HTML tag. |
| 21 | Easy | Which is the correct JSX attribute for CSS classes? | `class` | `className` | `css` | `styleClass` | B | `class` is a reserved word in JavaScript, so JSX uses `className`. |
| 22 | Easy | Which is a correctly self-closed JSX tag? | `<img src="x.png">` | `<br>` | `<input type="text" />` | `<br><br>` | C | JSX requires every tag to close; `<input ... />` is self-closing. |
| 23 | Medium | You write `count = 5` instead of `setCount(5)`. What happens on screen? | It updates to 5 | Nothing; React is not notified to re-render | It throws an error | The value resets to 0 | B | Direct assignment does not schedule a re-render in React. |
| 24 | Medium | You write `<button onClick={handleClick()}>`. When does `handleClick` run? | When the button is clicked | During render | Never | On page load and on click | B | The parentheses call the function immediately; use `onClick={handleClick}` or a wrapper. |
| 25 | Medium | A child component tries to reassign its `name` prop. What should it do instead? | Nothing — props are read-only | Call `setName` | Pass it back to the parent | Use `useState` | A | Props belong to the parent; the child should never mutate them. |
| 26 | Medium | You render a list with `people.map(...)`. What is the best `key`? | The array index | A random number | A stable unique id from the data | The person's first name | C | Use a stable id so React can correctly track each item when the list changes. |
| 27 | Easy | In `useState(0)`, which call makes React re-render? | Assigning the variable directly | Calling the setter | Reading the variable | Passing the initial value again | B | Only the setter function tells React to update the UI. |
| 28 | Hard | In Python, what makes indentation significant? | It is just a style guide | It is part of the syntax and determines code blocks | It helps the formatter | It adds comments | B | Python uses indentation to group statements inside functions, loops and conditionals. |
| 29 | Medium | You type `def get_project(project_id: int):` with `@app.get("/projects/{project_id}")`. What happens when the request sends `abc` as the id? | The route still runs with `abc` | FastAPI returns a `422` validation error | The server crashes | It is coerced to `0` | B | FastAPI uses the `int` type hint to validate and reject non-integer path values. |
| 30 | Medium | Which status code should a successful `POST /projects` return? | 200 | 201 | 404 | 204 | B | `201 Created` is the correct code for a successful creation. |

---

## Part II — Practical Coding (5 points each)

### 31. Semantic Portfolio Skeleton (Easy)

**Question:** Write a complete, valid HTML5 page skeleton for a portfolio. It must include `<!DOCTYPE html>`, `<html lang="en">`, a `<head>` with charset and viewport, a meaningful `<title>`, a `<body>` with `<header>`, `<nav>` (two links), `<main>` with two `<section>` elements, and `<footer>`.

**Answer:**
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

### 32. Fix Div Soup (Easy)

**Question:** The markup below is built only from `div`s. Replace each `div` with the correct semantic element.

```html
<div class="top">
  <div class="big">My Blog</div>
  <div class="menu">...</div>
</div>
<div class="main">
  <div class="post">...</div>
</div>
```

**Answer:**
```html
<header>
  <h1>My Blog</h1>
  <nav>...</nav>
</header>
<main>
  <article>...</article>
</main>
```

### 33. Fix Heading Hierarchy (Easy)

**Question:** Fix the heading hierarchy so the outline is logical.

```html
<h1>My Portfolio</h1>
<h4>About Me</h4>
<h2>Projects</h2>
<h4>Contact</h4>
```

**Answer:**
```html
<h1>My Portfolio</h1>
<h2>About Me</h2>
<h2>Projects</h2>
<h2>Contact</h2>
```

### 34. Article with Figure (Easy)

**Question:** Create an `<article>` that has an `<h2>` title, a `<figure>` containing an `<img>` with meaningful `alt` text, and a `<figcaption>`.

**Answer:**
```html
<article>
  <h2>Weather App</h2>
  <figure>
    <img src="weather.png" alt="Weather dashboard showing a five-day forecast for Manila">
    <figcaption>Weather App screenshot</figcaption>
  </figure>
</article>
```

### 35. Accessible Contact Form (Medium)

**Question:** Write a semantic, accessible contact form with `name`, `email`, `message` and a submit button. Each input must have a `<label>` and an `id`/`for` link.

**Answer:**
```html
<form>
  <label for="name">Name</label>
  <input type="text" id="name" name="name">

  <label for="email">Email</label>
  <input type="email" id="email" name="email">

  <label for="message">Message</label>
  <textarea id="message" name="message"></textarea>

  <button type="submit">Send</button>
</form>
```

### 36. Fix Bad Alt Text and Missing Labels (Medium)

**Question:** The form below has accessibility issues. Write the corrected HTML.

```html
<img src="p1.png" alt="p1.png">
<input type="text" placeholder="Email">
<p style="color:red">Invalid email</p>
```

**Answer:**
```html
<img src="p1.png" alt="Inventory dashboard showing low-stock alerts">
<label for="email">Email</label>
<input type="text" id="email">
<p class="error">Error: invalid email</p>
```

### 37. Missing Lang and Viewport (Easy)

**Question:** Complete the `<html>` and `<head>` of the page below.

```html
<!DOCTYPE html>
<html>
<head>
  <title>Portfolio</title>
</head>
```

**Answer:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfolio</title>
</head>
```

### 38. Deployment Pipeline (Easy)

**Question:** List the five steps that take a page from a local folder to a live URL and keep it updated with every push.

**Answer:**
1. Commit the files locally with `git commit`.
2. Push to a GitHub repository with `git push`.
3. Connect the repository to a static host (Netlify / Cloudflare Pages).
4. The host copies the files to its CDN and gives a public URL.
5. Every later `git push` triggers a rebuild and republishes the site.

### 39. Link Stylesheet (Easy)

**Question:** The CSS file `styles.css` is not being applied. Write the correct line to include it.

**Answer:**
```html
<link rel="stylesheet" href="styles.css">
```

### 40. Basic Text Styles (Easy)

**Question:** Write a CSS rule for `body` with `font-family: 'Calibri', Arial, sans-serif`, `font-size: 16px`, `line-height: 1.5`, `color: #2B2D42`, and a `.muted` class with `#676C8A`.

**Answer:**
```css
body {
  font-family: 'Calibri', Arial, sans-serif;
  font-size: 16px;
  line-height: 1.5;
  color: #2B2D42;
}
.muted { color: #676C8A; }
```

### 41. Flexbox Centering (Easy)

**Question:** Write CSS to center a `.hero` box both horizontally and vertically in the viewport using flexbox.

**Answer:**
```css
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
```

### 42. Box Model Overflow (Medium)

**Question:** A card with `width: 300px; padding: 20px; border: 1px solid #ccc;` is wider than expected. Write the single rule that makes the declared width the total width.

**Answer:**
```css
* { box-sizing: border-box; }
```
After this, `width: 300px` includes padding and border.

### 43. Responsive Nav Bar (Medium)

**Question:** Write CSS for a `.nav` that puts the site name on the left, links on the right, vertically centered, with `16px` space between links using flexbox.

```html
<nav class="nav">
  <span>Ana Cruz</span>
  <div class="links">
    <a href="#">Work</a>
    <a href="#">About</a>
    <a href="#">Contact</a>
  </div>
</nav>
```

**Answer:**
```css
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.links {
  display: flex;
  gap: 16px;
}
```

### 44. Tailwind Card Utilities (Medium)

**Question:** Convert this CSS into one Tailwind class string for a `<div>`.

```css
.card {
  padding: 16px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 16px;
}
```

**Answer:**
```html
<div class="p-4 bg-white rounded-lg flex items-center gap-4">...</div>
```

### 45. CSS to Tailwind Conversion (Medium)

**Question:** Convert the following CSS to a single Tailwind class string.

```css
.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 32px;
  background: navy;
  color: white;
}
```

**Answer:**
```html
<div class="flex justify-center items-center p-8 bg-navy text-white">...</div>
```

### 46. Responsive Card Gallery (Medium)

**Question:** Write a Tailwind class string that gives a grid: 1 column on phones, 2 columns from `768px`, and 3 columns from `1024px`, with `24px` gaps.

**Answer:**
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">...</div>
```

### 47. Debug className in JSX (Easy)

**Question:** Fix the JSX below.

```jsx
function Card() {
  return <div class="card">Hello</div>;
}
```

**Answer:**
```jsx
function Card() {
  return <div className="card">Hello</div>;
}
```

### 48. Debug Adjacent JSX Elements (Easy)

**Question:** The component below has multiple sibling elements. Fix it using a fragment.

```jsx
export default function App() {
  return (
    <h1>Title</h1>
    <p>Subtitle</p>
  );
}
```

**Answer:**
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

### 49. Counter Component (Medium)

**Question:** Build a React `Counter` that starts at `0` and shows `You have clicked the button {count} times.` with a button that increments `count`. Use a fragment.

**Answer:**
```jsx
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <>
      <p>You have clicked the button {count} times.</p>
      <button onClick={() => setCount(count + 1)}>Click me</button>
    </>
  );
}
```

### 50. Multi-Input Registration Form (Medium)

**Question:** Build a form with `name` and `email` stored in a single state object. On submit, log the state and prevent default submission.

**Answer:**
```jsx
import { useState } from "react";

export default function App() {
  const [form, setForm] = useState({ name: "", email: "" });

  function handleSubmit(e) {
    e.preventDefault();
    console.log(form);
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Name"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />
      <input
        type="email"
        placeholder="Email"
        value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 51. Controlled Name Input (Medium)

**Question:** Build a controlled input that displays `Hello, {name}` as the user types.

**Answer:**
```jsx
import { useState } from "react";

export default function App() {
  const [name, setName] = useState("");

  return (
    <div>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <p>Hello, {name}</p>
    </div>
  );
}
```

### 52. Toggle Contact Details (Medium)

**Question:** Build a component with a button labeled "Show contact". Clicking it reveals an email and changes the label to "Hide contact"; clicking again hides it.

**Answer:**
```jsx
import { useState } from "react";

export default function App() {
  const [show, setShow] = useState(false);

  return (
    <div>
      <button onClick={() => setShow(!show)}>
        {show ? "Hide contact" : "Show contact"}
      </button>
      {show && <p>ana@mail.com</p>}
    </div>
  );
}
```

### 53. Debug Index as Key (Medium)

**Question:** The list below uses the array index as `key`. Fix it.

```jsx
<ul>
  {projects.map((p, index) => (
    <li key={index}>{p.title}</li>
  ))}
</ul>
```

**Answer:**
```jsx
<ul>
  {projects.map((p) => (
    <li key={p.id}>{p.title}</li>
  ))}
</ul>
```

### 54. FastAPI Hello World (Easy)

**Question:** Write a FastAPI app with a single `GET /` route that returns `{"message": "Hello from the server"}`.

**Answer:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from the server"}
```

### 55. Path Parameter Route (Easy)

**Question:** Add a `GET /projects/{project_id}` route that returns `{"id": project_id, "title": "Weather App"}` and validates the id as an integer.

**Answer:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    return {"id": project_id, "title": "Weather App"}
```

### 56. GET /projects List (Medium)

**Question:** Write a route that returns a list of project dictionaries.

**Answer:**
```python
@app.get("/projects")
def list_projects():
    return [
        {"id": 1, "title": "Weather App", "tech": "React"},
        {"id": 2, "title": "Inventory", "tech": "FastAPI"},
    ]
```

### 57. POST with Pydantic (Medium)

**Question:** Create a Pydantic model `Project` with `title`, `tech` and optional `stars` (default `0`), and a `POST /projects` route that confirms creation.

**Answer:**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
    title: str
    tech: str
    stars: int = 0

@app.post("/projects")
def create_project(project: Project):
    return {"created": project.title, "tech": project.tech, "stars": project.stars}
```

### 58. Debug 200 Not 201 (Easy)

**Question:** The `POST /projects` route below returns `200`. Fix it to return `201`.

```python
@app.post("/projects")
def create_project(project: Project):
    return project
```

**Answer:**
```python
@app.post("/projects", status_code=201)
def create_project(project: Project):
    return project
```

### 59. 404 as Exception (Medium)

**Question:** The `GET /projects/{project_id}` route below returns a normal `200` with `"not found"` in the body. Fix it to return a proper `404`.

```python
@app.get("/projects/{project_id}")
def get_project(project_id: int):
    if project_id != 1:
        return {"error": "Project not found"}
    return {"id": 1, "title": "Weather App"}
```

**Answer:**
```python
from fastapi import HTTPException

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    if project_id != 1:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": 1, "title": "Weather App"}
```

### 60. In-Memory CRUD API (Hard)

**Question:** Build a full in-memory CRUD API for `projects` with `GET /projects`, `GET /projects/{project_id}` (404 if not found), `POST /projects` (201), and `DELETE /projects/{project_id}` (204, or 404 if not found). Use a Pydantic creation model and auto-incrementing IDs.

**Answer:**
```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class ProjectCreate(BaseModel):
    title: str
    tech: str

class Project(BaseModel):
    project_id: int
    title: str
    tech: str

projects_db: list[Project] = []
_next_id = 1

@app.get("/projects")
def list_projects():
    return projects_db

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    for project in projects_db:
        if project.project_id == project_id:
            return project
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate):
    global _next_id
    project = Project(project_id=_next_id, title=project_in.title, tech=project_in.tech)
    projects_db.append(project)
    _next_id += 1
    return project

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    for i, project in enumerate(projects_db):
        if project.project_id == project_id:
            projects_db.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
```
