# WST 60-Item Prelim Exam (Question Sheet)

**Instructions:** Part I has 30 multiple-choice questions (2 points each). Part II has 30 practical questions (5 points each). Total: 210 points. The answer key is in a separate file: `WST-Prelim-Exam-60-Answer-Key.md`.

---

## Part I — Multiple Choice (2 points each)

| # | Difficulty | Question | A | B | C | D |
| --- | ----------- | ---------- | --- | --- | --- | --- |
| 1 | Easy | Two pages look the same; one uses `div`, the other uses semantic elements. Who can tell the difference? | Only the browser | Only developers reading the source | Screen readers, search engines and other developers | Nobody |
| 2 | Easy | What does a static host actually do? | Runs Python code for free | Serves files as-is | Validates forms server-side | Compiles React |
| 3 | Easy | Which line in the `<head>` makes responsive CSS work on phones? | `<meta charset="UTF-8">` | `<meta name="viewport" content="width=device-width, initial-scale=1.0">` | `<link rel="stylesheet" href="styles.css">` | `<title>Portfolio</title>` |
| 4 | Medium | Why is it wrong to change an `<h2>` to `<h4>` just to make the text smaller? | It makes the page load slower | It breaks the document outline to fix a styling problem | It improves accessibility by adding hierarchy | It makes the text inaccessible |
| 5 | Easy | A decorative background image is an `<img>`. What should its `alt` be? | A full description of the flourish | The filename | `alt=""` | Omit the `alt` attribute |
| 6 | Easy | A form uses only `placeholder="Email"` instead of a `<label>`. What is the main problem? | It is harder to style | The hint disappears when the user types and may not be announced | The form will not submit | It takes too much space |
| 7 | Medium | Why can't the browser connect directly to the database? | It would require sending DB credentials to the user | Browsers cannot make network requests | HTML does not support databases | It is too slow |
| 8 | Medium | What does it mean that HTTP is stateless? | It is always encrypted | Each request is independent unless something extra carries identity | The server forgets everything automatically | Cookies are not allowed |
| 9 | Easy | What happens right after you run `git add .`? | Changes are committed | Changes are pushed to GitHub | Changes are staged for the next commit | Changes are deleted |
| 10 | Medium | Two functions each multiply a total by `1.12` to add VAT. Which principle is violated? | YAGNI | DRY | SOLID | KISS |
| 11 | Medium | You build tags, comments and a draft workflow that were not requested. Which principle is this? | DRY | SOLID | YAGNI | OOP |
| 12 | Medium | A single class validates input, hashes passwords, saves users and sends email. Which SOLID letter is broken? | S — Single Responsibility | O — Open/Closed | L — Liskov | D — Dependency Inversion |
| 13 | Hard | A route handler calls `psycopg.connect()` directly inside the function. What is the main cost? | It makes the code harder to read | It hard-wires the code to one database and makes testing difficult | It violates the Open/Closed principle | It leaks secrets into the front end |
| 14 | Easy | Which of these should be in `.gitignore`? | `main.py` | `README.md` | `.venv/` | `requirements.txt` |
| 15 | Medium | Which selector wins over `.lead` regardless of source order? | `p { }` | `.lead { }` | `#intro { }` | `*` |
| 16 | Medium | What does `box-sizing: border-box` do? | Adds a visible border | Includes padding and border in the declared width | Removes margins | Forces a square box |
| 17 | Medium | A paragraph has `margin-bottom: 20px` and the next has `margin-top: 20px`. What is the gap between them? | 40px | 20px | 0px | 30px |
| 18 | Easy | In Tailwind, `p-4` is equivalent to which padding? | 4px | 8px | 16px | 32px |
| 19 | Medium | In Tailwind's mobile-first model, an unprefixed utility class applies... | only on desktop | at 0px and above unless a breakpoint overrides it | only on phones | inside media queries only |
| 20 | Easy | Why must a React component name start with a capital letter? | It is a style rule | React uses capitalization to tell components from HTML tags | Faster rendering | Required by Babel |
| 21 | Easy | Which is the correct JSX attribute for CSS classes? | `class` | `className` | `css` | `styleClass` |
| 22 | Easy | Which is a correctly self-closed JSX tag? | `<img src="x.png">` | `<br>` | `<input type="text" />` | `<br><br>` |
| 23 | Medium | You write `count = 5` instead of `setCount(5)`. What happens on screen? | It updates to 5 | Nothing; React is not notified to re-render | It throws an error | The value resets to 0 |
| 24 | Medium | You write `<button onClick={handleClick()}>`. When does `handleClick` run? | When the button is clicked | During render | Never | On page load and on click |
| 25 | Medium | A child component tries to reassign its `name` prop. What should it do instead? | Nothing — props are read-only | Call `setName` | Pass it back to the parent | Use `useState` |
| 26 | Medium | You render a list with `people.map(...)`. What is the best `key`? | The array index | A random number | A stable unique id from the data | The person's first name |
| 27 | Easy | In `useState(0)`, which call makes React re-render? | Assigning the variable directly | Calling the setter | Reading the variable | Passing the initial value again |
| 28 | Hard | In Python, what makes indentation significant? | It is just a style guide | It is part of the syntax and determines code blocks | It helps the formatter | It adds comments |
| 29 | Medium | You type `def get_project(project_id: int):` with `@app.get("/projects/{project_id}")`. What happens when the request sends `abc` as the id? | The route still runs with `abc` | FastAPI returns a `422` validation error | The server crashes | It is coerced to `0` |
| 30 | Medium | Which status code should a successful `POST /projects` return? | 200 | 201 | 404 | 204 |

---
## Part II — Practical Coding (5 points each)

### 31. Semantic Portfolio Skeleton (Easy)

**Question:** Write a complete, valid HTML5 page skeleton for a portfolio. It must include `<!DOCTYPE html>`, `<html lang="en">`, a `<head>` with charset and viewport, a meaningful `<title>`, a `<body>` with `<header>`, `<nav>` (two links), `<main>` with two `<section>` elements, and `<footer>`.
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
### 33. Fix Heading Hierarchy (Easy)

**Question:** Fix the heading hierarchy so the outline is logical.

```html
<h1>My Portfolio</h1>
<h4>About Me</h4>
<h2>Projects</h2>
<h4>Contact</h4>
```
### 34. Article with Figure (Easy)

**Question:** Create an `<article>` that has an `<h2>` title, a `<figure>` containing an `<img>` with meaningful `alt` text, and a `<figcaption>`.
### 35. Accessible Contact Form (Medium)

**Question:** Write a semantic, accessible contact form with `name`, `email`, `message` and a submit button. Each input must have a `<label>` and an `id`/`for` link.
### 36. Fix Bad Alt Text and Missing Labels (Medium)

**Question:** The form below has accessibility issues. Write the corrected HTML.

```html
<img src="p1.png" alt="p1.png">
<input type="text" placeholder="Email">
<p style="color:red">Invalid email</p>
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
### 38. Deployment Pipeline (Easy)

**Question:** List the five steps that take a page from a local folder to a live URL and keep it updated with every push.
### 39. Link Stylesheet (Easy)

**Question:** The CSS file `styles.css` is not being applied. Write the correct line to include it.
### 40. Basic Text Styles (Easy)

**Question:** Write a CSS rule for `body` with `font-family: 'Calibri', Arial, sans-serif`, `font-size: 16px`, `line-height: 1.5`, `color: #2B2D42`, and a `.muted` class with `#676C8A`.
### 41. Flexbox Centering (Easy)

**Question:** Write CSS to center a `.hero` box both horizontally and vertically in the viewport using flexbox.
### 42. Box Model Overflow (Medium)

**Question:** A card with `width: 300px; padding: 20px; border: 1px solid #ccc;` is wider than expected. Write the single rule that makes the declared width the total width.
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
### 46. Responsive Card Gallery (Medium)

**Question:** Write a Tailwind class string that gives a grid: 1 column on phones, 2 columns from `768px`, and 3 columns from `1024px`, with `24px` gaps.
### 47. Debug className in JSX (Easy)

**Question:** Fix the JSX below.

```jsx
function Card() {
  return <div class="card">Hello</div>;
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
### 49. Counter Component (Medium)

**Question:** Build a React `Counter` that starts at `0` and shows `You have clicked the button {count} times.` with a button that increments `count`. Use a fragment.
### 50. Multi-Input Registration Form (Medium)

**Question:** Build a form with `name` and `email` stored in a single state object. On submit, log the state and prevent default submission.
### 51. Controlled Name Input (Medium)

**Question:** Build a controlled input that displays `Hello, {name}` as the user types.
### 52. Toggle Contact Details (Medium)

**Question:** Build a component with a button labeled "Show contact". Clicking it reveals an email and changes the label to "Hide contact"; clicking again hides it.
### 53. Debug Index as Key (Medium)

**Question:** The list below uses the array index as `key`. Fix it.

```jsx
<ul>
  {projects.map((p, index) => (
    <li key={index}>{p.title}</li>
  ))}
</ul>
```
### 54. FastAPI Hello World (Easy)

**Question:** Write a FastAPI app with a single `GET /` route that returns `{"message": "Hello from the server"}`.
### 55. Path Parameter Route (Easy)

**Question:** Add a `GET /projects/{project_id}` route that returns `{"id": project_id, "title": "Weather App"}` and validates the id as an integer.
### 56. GET /projects List (Medium)

**Question:** Write a route that returns a list of project dictionaries.
### 57. POST with Pydantic (Medium)

**Question:** Create a Pydantic model `Project` with `title`, `tech` and optional `stars` (default `0`), and a `POST /projects` route that confirms creation.
### 58. Debug 200 Not 201 (Easy)

**Question:** The `POST /projects` route below returns `200`. Fix it to return `201`.

```python
@app.post("/projects")
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
### 60. In-Memory CRUD API (Hard)

**Question:** Build a full in-memory CRUD API for `projects` with `GET /projects`, `GET /projects/{project_id}` (404 if not found), `POST /projects` (201), and `DELETE /projects/{project_id}` (204, or 404 if not found). Use a Pydantic creation model and auto-incrementing IDs.
