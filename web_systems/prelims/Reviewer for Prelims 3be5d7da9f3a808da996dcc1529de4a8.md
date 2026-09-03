# Reviewer for Prelims

### REACT.JS part

```jsx
import { useState } from 'react';

// The root component name must use PascalCase (capitalized)
export default function App() {
  const [count, setCount] = useState(0);
  const title = "Welcome to My React App";

  // Event handler for button clicks
  const handleClick = () => {
    setCount(count + 1);
  };

  return (
    // <> is a React Fragment used to wrap adjacent elements without rendering an extra <div>
    <>
      <header className="app-header">
        {/* Dynamic JavaScript expressions are embedded within curly braces */}
        <h1>{title}</h1>
      </header>
      
      <main>
        <p>You have clicked the button {count} times.</p>
        {/* Use camelCase for event handlers like onClick */}
        <button onClick={handleClick}>
          Click Me
        </button>
      </main>
    </>
  );
}
```

```jsx
import React from 'react';

function FruitList() {
  const fruits = ['Apple', 'Banana', 'Orange'];

  return (
    <ul>
      {fruits.map((fruit, index) => (
        <li key={index}>{fruit}</li>
      ))}
    </ul>
  );
}

export default FruitList;
```

# Styling the Web: CSS & Tailwind CSS

**Web Systems and Technologies · BSCS 4122 / 4122L**
University of Perpetual Help System DALTA · College of Computer Studies
First Semester, School Year 2025–2026 · Student companion material

## Contents

1. What CSS Is and How to Attach It
2. Selectors — Choosing What to Style
3. The Box Model
4. Colour, Text and Units
5. Layout with Flexbox
6. Layout with Grid
7. Responsive Design
8. Tailwind CSS — Utility-First Styling
9. Tailwind in Practice
10. Quick Reference & Glossary

**Prerequisite:** Comfortable with semantic HTML, working editor, Node.js, and a page of your own to style.

---

## Part 1 — What CSS Is and How to Attach It

CSS (Cascading Style Sheets) controls how HTML looks: colour, spacing, size, position, and layout. HTML gives a page its meaning and structure; CSS gives it its appearance. The two are deliberately separate, so the same markup can be restyled without touching its content.

### Three ways to add CSS

```html
<!-- 1. INLINE: on the element. Avoid — hard to reuse and maintain -->
<p style="color: navy;">Hello</p>

<!-- 2. INTERNAL: a <style> block in the <head>. Fine for one small page -->
<style>
  p { color: navy; }
</style>

<!-- 3. EXTERNAL: a separate .css file. This is what professionals use -->
<link rel="stylesheet" href="styles.css">
```

> **Use external stylesheets.** One `styles.css` file styles every page, lives in version control, and keeps your HTML clean. Inline styles are the CSS equivalent of shouting over your own structure.
> 

### The anatomy of a rule

```css
selector {
  property: value; /* this line is a "declaration" */
  color: navy;
  font-size: 18px;
}
/* selector -> WHAT you are styling (here, every <h1>)
   property -> WHICH aspect (color, font-size, margin...)
   value -> the setting for that property
   declaration -> one property: value; pair
   { ... } -> the declaration block */
```

### Why it is called "cascading"

Several rules can target the same element. When they conflict, CSS decides the winner using three ideas, checked in order:

1. **Importance and origin** — later rules and more specific sources win.
2. **Specificity** — an id beats a class, which beats an element name.
3. **Source order** — if everything else ties, the rule written last wins.

> **The one-sentence version:** When two rules fight, the more specific one wins; if they are equally specific, the last one written wins.
> 

### Exercise 1

Create a `styles.css`, link it to your HTML page, and turn every `<h1>` navy and every paragraph dark grey. Then add an internal `<style>` rule that makes one specific paragraph red, and predict which colour wins before you refresh.

---

## Part 2 — Selectors: Choosing What to Style

A selector answers one question: which elements does this rule apply to?

### The three you will use constantly

| Selector | Targets | Example |
| --- | --- | --- |
| `element` | Every tag of that type | `p { }` — all paragraphs |
| `.class` | Any element with that class | `.card { }` — `class="card"` |
| `#id` | The one element with that id | `#header { }` — `id="header"` |

> **Reach for classes.** Classes are reusable and easy to keep track of. Use ids sparingly — an id must be unique on the page, and its high specificity makes rules hard to override later.
> 

```css
h2 { color: navy; }                /* element */
.btn { padding: 10px; }            /* class */
#main-title { font-size: 40px; }   /* id */

/* combine them */
.card .title { font-weight: bold; }  /* a .title INSIDE a .card (descendant) */
.card > p { margin: 0; }             /* a <p> that is a DIRECT child of .card */
button:hover { background: navy; }   /* a button while the mouse is over it */
input:focus { border-color: teal; }  /* an input while it is selected */
```

### Specificity, briefly

| Selector type | Weight | Beaten by |
| --- | --- | --- |
| Element — `p` | Lowest | class, id |
| Class — `.card` | Middle | id |
| id — `#main` | High | inline style |
| Inline — `style="..."` | Highest | (avoid needing to) |

> **The specificity trap:** If you find yourself piling on `#id` selectors or reaching for `!important` to make a style stick, stop. It is almost always a sign your selectors are fighting each other. Simplify instead of escalating.
> 

### Exercise 2

Give three of your project cards the class `card`. Write one `.card` rule that styles all three at once. Then use `.card:hover` to change the background when the mouse is over a card.

---

## Part 3 — The Box Model

Every element on a page is a rectangular box, whether it looks like one or not.

### Four layers, from the inside out

| Layer | What it is | Property |
| --- | --- | --- |
| Content | The text or image itself | `width`, `height` |
| Padding | Space inside the box, around the content | `padding` |
| Border | The line around the padding | `border` |
| Margin | Space outside the box, pushing others away | `margin` |

> **Padding vs margin — the distinction students miss:** Padding is cushioning inside the box; it shares the box's background colour. Margin is empty space outside the box that separates it from its neighbours. Inside vs outside — that is the whole difference.
> 

```css
.card {
  width: 300px;
  padding: 20px;              /* space inside, around the text */
  border: 1px solid #ccc;     /* the visible edge */
  margin: 16px;                /* space outside, between cards */
}

/* shorthand: one value = all four sides */
padding: 20px;
/* two values = vertical horizontal */
padding: 10px 20px;
/* four values = top right bottom left (clockwise) */
padding: 10px 20px 10px 20px;
```

### The box-sizing fix everyone should know

By default, `width` sets only the content width. Padding and border are then added on top, so a box you set to 300px actually renders wider.

```css
/* Without this: width 300px + padding 20px + border 1px
   = 342px actual. Confusing. */

/* With this: width means the WHOLE box. Padding and
   border are included. Put it at the top of every project. */
* {
  box-sizing: border-box;
}
```

> **Start every stylesheet with `box-sizing: border-box`.** It makes width behave the way you expect — the number you set is the size you get. Tailwind applies this for you automatically.
> 

### The collapsing margin surprise

When two vertical margins meet — say a paragraph with `margin-bottom: 20px` above one with `margin-top: 20px` — they do not add up to 40px. They collapse to the larger of the two, 20px. This is normal, defined behaviour, not a bug.

### Exercise 3

Add `box-sizing: border-box` to your stylesheet. Give your project cards `padding: 20px`, a 1px border and `margin-bottom: 16px`. Open devtools, select a card, and find the box-model diagram — watch it match the four layers above.

---

## Part 4 — Colour, Text and Units

### Ways to write a colour

| Form | Example | Notes |
| --- | --- | --- |
| Named | `navy`, `tomato` | About 140 names. Handy for quick tests. |
| Hex | `#1A1B3A` | The most common form in real projects. |
| RGB | `rgb(26, 27, 58)` | Red, green, blue from 0–255. |
| RGBA | `rgba(26,27,58,0.5)` | The `a` is opacity, 0–1. |

### Styling text

```css
body {
  font-family: 'Calibri', Arial, sans-serif; /* fallbacks if the first is missing */
  font-size: 16px;
  line-height: 1.5; /* 1.5x the font size — good for readability */
  color: #2B2D42;
}

h1 { font-weight: bold; }
.muted { color: #676C8A; }
.center { text-align: center; }
```

### px, rem and % — which unit when

| Unit | Means | Use for |
| --- | --- | --- |
| `px` | Fixed pixels | Borders, small fixed details |
| `rem` | Relative to the root font size | Font sizes and spacing — scales with user settings |
| `%` | Relative to the parent | Widths in fluid layouts |

> **Prefer rem for type and spacing.** If a user increases their browser's default font size for readability, rem values grow with it and px values do not. Using rem is a small, free accessibility win.
> 

### Custom properties (CSS variables)

Define a value once, reuse it everywhere. Change it in one place, update the whole site.

```css
:root {
  --brand: #1A1B3A;
  --accent: #F08A24;
  --space: 16px;
}

.button {
  background: var(--brand);
  padding: var(--space);
}

.button:hover { background: var(--accent); }
```

> **Why this matters for Tailwind:** Tailwind is built on exactly this idea — a fixed set of named design values you reuse instead of typing raw numbers. Understanding custom properties now makes Tailwind feel familiar in Part 8.
> 

### Exercise 4

Define `--brand` and `--accent` colours in `:root`. Use them on your header and buttons. Change one variable and watch every element that uses it update at once.

---

## Part 5 — Layout with Flexbox

Flexbox arranges items in one direction — a row or a column. It is the right tool for nav bars, button groups, card rows, and centring things.

### The mental model: two axes

Set `display: flex` on a container, and its direct children become flex items laid out along the main axis. The cross axis runs perpendicular to it.

- `justify-content` aligns items along the main axis (usually horizontal).
- `align-items` aligns items along the cross axis (usually vertical).

```css
.nav {
  display: flex;                     /* turn on flexbox */
  justify-content: space-between;    /* spread items apart */
  align-items: center;               /* vertically centre them */
  gap: 16px;                         /* space between items */
}

/* common justify-content values:
   flex-start | center | flex-end | space-between | space-around */
```

### Perfect centring — the classic win

```css
.hero {
  display: flex;
  justify-content: center;  /* centre horizontally */
  align-items: center;      /* centre vertically */
  height: 100vh;             /* full viewport height */
}
```

| Property | Goes on | Does |
| --- | --- | --- |
| `display: flex` | container | Turns on flex layout |
| `flex-direction` | container | row (default) or column |
| `justify-content` | container | Aligns along the main axis |
| `align-items` | container | Aligns along the cross axis |
| `gap` | container | Space between items |
| `flex-wrap` | container | Let items wrap to a new line |

> **`gap` is your friend.** Use `gap` for spacing between flex items instead of adding margins to each child. Cleaner, and no stray margin on the last item.
> 

### Exercise 5

Turn your page's header into a flex container so your name sits on the left and your nav links on the right, vertically centred. Then lay your project cards in a wrapping flex row with a 24px gap.

---

## Part 6 — Layout with Grid

Where flexbox handles one direction, CSS Grid handles two — rows and columns at once. It is the right tool for page layouts and card galleries.

### Columns with fr and repeat

```css
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* three equal columns */
  gap: 20px;
}

/* repeat(3, 1fr) is shorthand for: 1fr 1fr 1fr
   fr = one share of the leftover space
   so three columns each take one third, evenly */
```

### A grid that adapts on its own

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

/* auto-fit -> make as many columns as fit
   minmax -> each at least 200px, at most 1 equal share
   result -> 4 columns on a laptop, 1 on a phone, automatically */
```

> **Flexbox or Grid?** Rough rule: Flexbox for one dimension (a row of buttons, a nav bar), Grid for two (a page layout, a gallery). They work together happily — a grid cell can itself be a flex container.
> 

### Exercise 6

Lay your project cards out with the `auto-fit`/`minmax` grid above. Resize the browser window from wide to narrow and watch the columns collapse from several down to one, with no extra code.

---

## Part 7 — Responsive Design

A responsive page works on any screen, from a narrow phone to a wide monitor.

### 1. The viewport tag

```html
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">
```

Without this one line in `<head>`, phones pretend to be a wide desktop and your responsive CSS is ignored.

### 2. Media queries

```css
/* base styles apply everywhere */
.container { padding: 16px; }

/* extra rules ONLY when the screen is 768px or wider */
@media (min-width: 768px) {
  .container { padding: 40px; }
  .cards { grid-template-columns: repeat(3, 1fr); }
}
```

### 3. Mobile-first thinking

Write the styles for the small screen first, as your base. Then use `min-width` media queries to add complexity as the screen grows. This is easier to reason about than starting wide and stripping things away, and it is the approach Tailwind is built around.

> **Common breakpoints:** 640px (large phone), 768px (tablet), 1024px (laptop), 1280px (desktop).
> 

### Exercise 7

Give your card grid one column by default. Add a media query at 768px that switches it to three columns. Narrow your browser to confirm the phone layout, then widen it to see the desktop layout appear.

---

## Part 8 — Tailwind CSS: Utility-First Styling

Everything so far was plain CSS. Tailwind does not replace what you learned — it is a faster way to apply it. Instead of writing rules in a separate file, you compose small utility classes directly on your elements.

### The same card, two ways

**Plain CSS**

```css
/* styles.css */
.card {
  padding: 16px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,.1);
}
```

```html
<!-- index.html -->
<div class="card">...</div>
```

**Tailwind**

```html
<!-- no separate CSS file needed -->
<div class="p-4 bg-white rounded-lg shadow">
  ...
</div>
<!-- p-4 = padding: 16px
     bg-white = background: white
     rounded = border-radius
     shadow = box-shadow -->
```

### Why utilities instead of custom classes

- You stop naming things. No more inventing `.card-inner-wrapper-left`. The classes describe what they do.
- You stay in one file. Markup and style sit together, which pairs naturally with React components.
- The design stays consistent. `p-4` is always 16px. You pick from a fixed scale instead of typing arbitrary numbers.
- Unused styles are stripped. The final CSS file only contains the utilities you actually used, so it stays small.

> **The honest downside:** Class lists get long, and markup can look busy at first: `class="flex items-center justify-between p-4"`. This feels strange coming from clean HTML. It reads much better once you know the vocabulary — and in React you will wrap repeated patterns in a component, so you write the long list once.
> 

### Setting it up with Vite

```bash
npm install tailwindcss @tailwindcss/vite
# then add the plugin in vite.config.js, and one line
# of CSS imports Tailwind:
# @import "tailwindcss";
#
# Full current steps live at tailwindcss.com — always
# follow the official guide for your version.
```

> **Setup changes between versions.** Tailwind's install steps have changed across recent versions. Do not memorise them — follow the current official guide at tailwindcss.com/docs for the version you install. Reading official docs is itself a course skill.
> 

### The mental map from CSS to Tailwind

| You know (CSS) | Tailwind class |
| --- | --- |
| `padding: 16px` | `p-4` |
| `margin-top: 8px` | `mt-2` |
| `display: flex` | `flex` |
| `color: white` | `text-white` |
| `font-size: 1.5rem` | `text-2xl` |
| `border-radius: 8px` | `rounded-lg` |

The number scale is consistent: `p-1` = 4px, `p-2` = 8px, `p-4` = 16px, `p-8` = 32px. Each step is 4px.

---

## Part 9 — Tailwind in Practice

### Spacing, colour and text

```html
<div class="p-6 m-4 bg-white text-gray-800 rounded-lg shadow">
  <h2 class="text-2xl font-bold text-navy">Project Title</h2>
  <p class="mt-2 text-sm text-gray-500">Built with React</p>
</div>
<!-- p-6 padding · m-4 margin · bg-white background
     text-2xl size · font-bold weight · mt-2 margin-top
     text-gray-500 a muted grey · rounded-lg · shadow -->
```

### Flexbox and Grid, the Tailwind way

**Flex — a nav bar**

```html
<nav class="flex items-center justify-between p-4">
  <span>Your Name</span>
  <div class="flex gap-4">
    <a href="#">Work</a>
    <a href="#">Contact</a>
  </div>
</nav>
```

**Grid — a card gallery**

```html
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div>Card</div>
  <div>Card</div>
  <div>Card</div>
</div>
```

### Responsive prefixes — the best idea in Tailwind

Prefix any utility with a breakpoint and it only applies at that size and up. This is a media query, written inline, mobile-first.

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  ...
</div>
<!-- grid-cols-1 -> 1 column by default (phones)
     md:grid-cols-2 -> 2 columns from 768px up
     lg:grid-cols-4 -> 4 columns from 1024px up
     The same responsive card grid from Part 6, in one line. -->
```

### Hover and focus states

```html
<button class="bg-navy text-white px-4 py-2 rounded hover:bg-orange focus:ring">
  Contact me
</button>
<!-- hover:bg-orange -> change background on hover
     focus:ring -> show a focus ring for keyboard users
     Keeps keyboard users and hover states in mind. -->
```

### The payoff in React

```jsx
// Card.jsx
function Card({ title, tech }) {
  return (
    <div className="p-6 bg-white rounded-lg shadow hover:shadow-lg">
      <h3 className="text-xl font-bold">{title}</h3>
      <p className="mt-2 text-sm text-gray-500">{tech}</p>
    </div>
  );
}
// write the styling once, render it many times
```

> **Note: className, not class.** Inside React and JSX it is `className`, because `class` is a reserved word in JavaScript. In a plain `.html` file it stays `class`.
> 

### Exercise 8

Rebuild your portfolio's project card with Tailwind utilities instead of a CSS file: padding, a white background, rounded corners, a shadow, and a hover that deepens the shadow. Then make the card grid `grid-cols-1 md:grid-cols-3` and resize to test it.

---

## Part 10 — Quick Reference & Glossary

### CSS to Tailwind cheat sheet

| Goal | CSS | Tailwind |
| --- | --- | --- |
| Padding 16px | `padding: 16px` | `p-4` |
| Margin top 8px | `margin-top: 8px` | `mt-2` |
| Flex row, centred | `display:flex; align-items:center` | `flex items-center` |
| Space items apart | `justify-content: space-between` | `justify-between` |
| Gap between items | `gap: 16px` | `gap-4` |
| 3-column grid | `grid-template-columns: repeat(3,1fr)` | `grid grid-cols-3` |
| White background | `background: white` | `bg-white` |
| Grey text | `color: #6b7280` | `text-gray-500` |
| Bold, large | `font-weight:bold; font-size:1.5rem` | `font-bold text-2xl` |
| Rounded corners | `border-radius: 8px` | `rounded-lg` |
| On hover | `:hover { ... }` | `hover:...` |
| From tablet up | `@media (min-width:768px)` | `md:...` |

### Common mistakes to avoid

| Mistake | Fix |
| --- | --- |
| Forgetting `box-sizing: border-box` | Add it at the top; widths behave predictably |
| Confusing padding (inside) with margin (outside) | Inside the box vs space between boxes |
| Fighting specificity with `!important` | Simplify selectors instead of escalating |
| Missing the viewport meta tag | Responsive CSS is ignored on phones without it |
| Writing `class` in JSX | Use `className` in React |
| Memorising Tailwind setup steps | Follow the current official docs for your version |

### Glossary

| Term | Meaning |
| --- | --- |
| Selector | The part of a CSS rule that chooses which elements to style |
| Declaration | One `property: value;` pair |
| Specificity | The score CSS uses to decide which conflicting rule wins |
| Box model | Content, padding, border, margin — the four layers of every element |
| Flexbox | One-dimensional layout, a row or a column |
| Grid | Two-dimensional layout, rows and columns together |
| Media query | CSS that applies only when a screen condition is met |
| Breakpoint | A screen width where the layout changes |
| Utility class | A Tailwind class that sets one specific style |
| `fr` unit | In Grid, one fraction of the available free space |

### Where to go next

Keep two references open while you build: developer.mozilla.org for CSS, and tailwindcss.com/docs for Tailwind. Learning to read official documentation is a course outcome in its own right — it is the skill that stays useful after every specific detail here has changed.

---

*End of guide · Web Systems and Technologies · College of Computer Studies*

# The Server Side: Python & FastAPI

**Web Systems and Technologies · BSCS 4122 / 4122L**
University of Perpetual Help System DALTA · College of Computer Studies
First Semester, School Year 2026–2027 · Student companion material

## Contents

1. What the Back End Is and Why It Exists
2. Python for People Who Know JavaScript
3. Setting Up Your Environment
4. Your First FastAPI Application
5. Routes and HTTP Methods
6. Path and Query Parameters
7. Request Bodies with Pydantic
8. Responses and Status Codes
9. Putting It Together
10. Quick Reference & Glossary

**Prerequisite:** You can build and style a page, you understand the request–response cycle, and you have Python and an editor installed. No prior Python experience is assumed.

---

## Part 1 — What the Back End Is and Why It Exists

Everything you have built so far runs in the browser — the front end. It is the part the user sees and can inspect. The back end is the code that runs on a machine you control, that the browser talks to over the network. It answers requests, enforces the rules, and is the only part allowed near your real data.

### The split, one more time

|  | Front end (browser) | Back end (server) |
| --- | --- | --- |
| Runs on | The user's device | A machine you control |
| Made of | HTML, CSS, JavaScript, React | Python, FastAPI |
| Can be trusted? | No — the user controls it | Yes — you control it |
| Talks to the database? | Never directly | Yes, this is its job |

### What only the server can do

- **Hold secrets.** Database passwords and API keys live here, never in front-end code the user can read.
- **Enforce the rules.** "Can this user delete this record?" is decided on the server, where it cannot be bypassed.
- **Talk to the database.** The browser asks the server; the server queries the data and answers.
- **Do the real work.** Processing, calculations, sending email — anything that must be reliable.

> **The rule from the front-end material, now from the other side:** Anything in the browser can be edited by the user, so front-end checks are for convenience only. The back end is where safety actually lives. When you validate here, the user cannot get around it — which is exactly why this layer exists.
> 

### What an API is

Your back end exposes an API (Application Programming Interface) — a set of URLs the front end can call to read or change data. Your React app will send a request to a URL like `/projects`; your FastAPI code answers it. That contract between the two halves is what you are about to build.

### Exercise 1

In one or two sentences each, write down why each of these belongs on the server and not in the browser: your database password, the check for whether a user is allowed to edit a post, and the list of all users' email addresses.

---

## Part 2 — Python for People Who Know JavaScript

FastAPI is written in Python. The good news: you already think like a programmer. Variables, functions, conditions, lists — the ideas are identical. Mostly you are learning new spelling.

### The translation table

| Idea | JavaScript | Python |
| --- | --- | --- |
| Variable | `const x = 5;` | `x = 5` |
| Function | `function f(a) { }` | `def f(a):` |
| Return | `return a + 1;` | `return a + 1` |
| List / array | `[1, 2, 3]` | `[1, 2, 3]` |
| Object / dict | `{ name: "Ana" }` | `{"name": "Ana"}` |
| true / false | `true / false` | `True / False` |
| Nothing | `null` | `None` |
| Comment | `// note` | `# note` |
| Text join | ``Hi, ${n}`` | `f"Hi, {n}"` |

### The one big difference: whitespace matters

JavaScript uses curly braces to group code. Python uses indentation — the spaces at the start of a line are part of the syntax, not just style.

```python
def greet(name):
    if name == "Ana":              # colon, then indent
        return f"Hello, {name}"    # this line is inside the if
    return "Hello, stranger"       # this line is not

# a list and a dict
scores = [90, 75, 88]
student = {"name": "Ana", "year": 3}

student["name"]   # "Ana" — bracket access, like JS
len(scores)        # 3
```

> **Indentation is the syntax.** In Python, the indentation is how the language knows what is inside a function or an `if`. Mixing tabs and spaces, or getting the indent wrong, is a real error — not a style nitpick. Pick four spaces and let your editor keep them consistent.
> 

> **Type hints — you will see them everywhere in FastAPI.** Python lets you annotate types: `def add(a: int, b: int) -> int:`. They are optional in plain Python, but FastAPI uses them to validate requests and generate documentation automatically. Get used to reading them now.
> 

### Exercise 2

Write a Python function `total(prices)` that takes a list of numbers and returns their sum (try the builtin `sum()`). Then write one that takes a student dict and returns an f-string like `"Ana is in year 3"`.

---

## Part 3 — Setting Up Your Environment

Before writing any server code, you create an isolated space for this project's packages — a virtual environment. It keeps this project's dependencies separate from every other project on your machine.

### Create and activate

```bash
# make a project folder and enter it
mkdir projects-api
cd projects-api

# create a virtual environment named .venv
python -m venv .venv

# activate it
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

### Install FastAPI

```bash
# (with .venv active)
pip install "fastapi[standard]"
# this brings in FastAPI and uvicorn, the server
# that actually runs your app during development

# record your dependencies so others can rebuild:
pip freeze > requirements.txt
```

> **Two things that must never be committed:** Add both `.venv/` and any `.env` secrets file to your `.gitignore`. The virtual environment is generated (anyone can rebuild it from `requirements.txt`), and secrets must never enter version control. This is the habit that prevents a leaked database password later.
> 

> **Why the .venv, again:** Without it, every `pip install` lands system-wide, and two projects that need different versions of a package start breaking each other. One sealed environment per project is the fix, and `requirements.txt` is how a teammate — or a grader — recreates yours exactly.
> 

### Exercise 3

Create a new project folder, make and activate a `.venv`, install FastAPI, and run `pip freeze > requirements.txt`. Open the file and read what got installed. Add `.venv/` to a `.gitignore`.

---

## Part 4 — Your First FastAPI Application

A working API in a handful of lines. Create a file called `main.py`.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from the server"}
```

### Run it

```bash
fastapi dev main.py
# FastAPI starts the server and watches for changes.
# Open the URL it prints, usually:
# http://127.0.0.1:8000
```

Visit that URL and you will see your JSON response. You have a live back end.

### The free gift: interactive documentation

FastAPI reads your code and builds a live, clickable documentation page for your API automatically. Visit:

```
http://127.0.0.1:8000/docs
# An interactive page listing every endpoint.
# You can send real requests to your API from here —
# no extra tools needed to test it.
```

> **Read the /docs page from day one.** This automatic documentation is one of the best reasons to use FastAPI. Every route you add appears here instantly, with a form to try it. Use it to test your work throughout this course — it replaces a lot of manual clicking and guesswork.
> 

### What each piece means

| Code | Meaning |
| --- | --- |
| `app = FastAPI()` | Creates your application |
| `@app.get("/")` | Handle GET requests to the path `/` |
| `def read_root():` | The function that runs for that request |
| `return {...}` | FastAPI turns the dict into a JSON response |

### Exercise 4

Create `main.py`, run it, and confirm the JSON in your browser. Then open `/docs`, find your endpoint, and use the "Try it out" button to call it. Change the message, save, and watch the server reload.

---

## Part 5 — Routes and HTTP Methods

A route (or path operation) pairs a URL path with an HTTP method and the function that handles it.

### The four you will use

| Method | Means | Decorator |
| --- | --- | --- |
| GET | Read data | `@app.get(...)` |
| POST | Create new data | `@app.post(...)` |
| PUT | Update existing data | `@app.put(...)` |
| DELETE | Remove data | `@app.delete(...)` |

### Several routes in one app

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Projects API"}

@app.get("/projects")
def list_projects():
    return [{"id": 1, "title": "Weather App"}]

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

> **The decorator is the connection.** The line starting with `@` just above a function is a decorator. `@app.get("/projects")` tells FastAPI: when a GET request arrives for `/projects`, run this function. The function name is yours to choose; the path and method are what matter.
> 

> **Naming your paths:** Use nouns, not verbs, and plurals for collections: `/projects` for the list, `/projects/1` for one item. Let the HTTP method carry the action — `GET /projects` reads, `POST /projects` creates. You do not need `/getProjects` or `/createProject`.
> 

### Exercise 5

Add three GET routes to your app: `/` returning a welcome message, `/projects` returning a list of two project dicts, and `/about` returning your name and course. Test all three from `/docs`.

---

## Part 6 — Path and Query Parameters

Often the client needs to ask about a specific thing, or refine a request. Two ways carry that information in the URL.

### Path parameters — part of the address

Use them to identify one specific resource. The value in braces becomes an argument to your function.

```python
@app.get("/projects/{project_id}")
def get_project(project_id: int):
    return {"id": project_id, "title": "Weather App"}

# a request to /projects/5
# -> project_id is 5
# the type hint (: int) makes FastAPI convert and check it
```

### Query parameters — after the question mark

Use them to filter, sort or paginate. Any function argument that is not in the path becomes a query parameter.

```python
@app.get("/projects")
def list_projects(tech: str = "all", limit: int = 10):
    return {"tech": tech, "limit": limit}

# a request to /projects?tech=react&limit=5
# -> tech is "react", limit is 5
# the = gives each a default, so both are optional
```

> **Type hints do real work here.** Because you wrote `project_id: int`, a request to `/projects/abc` is automatically rejected with a clear error — FastAPI validated it before your function ever ran. You get input checking for free, just by naming the type.
> 

|  | Path parameter | Query parameter |
| --- | --- | --- |
| Looks like | `/projects/5` | `/projects?tech=react` |
| Use for | Identifying one item | Filtering or options |
| In the code | Name is in the path `{...}` | Name is not in the path |

### Exercise 6

Add a route `/projects/{project_id}` that returns a dict containing that id, typed as an `int`. Then add a query parameter `tech` to your `/projects` list route. Test both from `/docs`, and try `/projects/abc` to see the automatic error.

---

## Part 7 — Request Bodies with Pydantic

To create something, the client sends data in the body of a POST request. You describe the shape of that data with a Pydantic model, and FastAPI validates every incoming request against it automatically.

### Define the shape

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# a model is a class describing the expected data
class Project(BaseModel):
    title: str
    tech: str
    stars: int = 0   # a default makes this optional
```

### Accept it in a POST route

```python
@app.post("/projects")
def create_project(project: Project):
    # FastAPI has already validated the body and
    # given you a ready-to-use Project object
    return {"created": project.title, "tech": project.tech}
```

> **Validation you did not have to write.** Because the body is typed as `Project`, FastAPI checks it before your function runs. A missing `title`, or a `stars` that is not a number, is rejected automatically with a clear message saying exactly what was wrong. You declared the shape; the checking came free.
> 

> **This is the same instinct as the front end.** On the front end you learned never to trust raw input. Here the server enforces it for real: the model is a gate, and nothing malformed gets past it into your logic.
> 

The `/docs` page reads your model too — open it after adding this and the POST endpoint shows the exact fields it expects, with a form to send a test request.

### Exercise 7

Define a `Project` model with `title`, `tech`, and an optional `stars`. Add a POST `/projects` route that accepts it and returns a confirmation. From `/docs`, send a valid project, then send one missing the `title` and read the error FastAPI returns.

---

## Part 8 — Responses and Status Codes

Your function's return value becomes the response body — FastAPI converts a dict or list straight to JSON. Alongside the body, every response carries a status code, a number that tells the client what happened.

### The codes you will use most

| Code | Means | When |
| --- | --- | --- |
| 200 | OK | A successful GET (the default) |
| 201 | Created | A POST made something new |
| 404 | Not Found | The requested item does not exist |
| 422 | Unprocessable | The body failed validation (automatic) |
| 500 | Server Error | Something broke in your code |

### Setting a success code

```python
@app.post("/projects", status_code=201)
def create_project(project: Project):
    return {"created": project.title}
# a successful create now replies 201, not 200
```

### Reporting an error properly

When something is wrong — an item is missing — do not return a normal dict. Raise an `HTTPException` so the client gets the right status code.

```python
from fastapi import HTTPException

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    if project_id != 1:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )
    return {"id": 1, "title": "Weather App"}
```

> **Honest status codes matter.** Returning `200 OK` with a body that says "not found" lies to the client — and to the React code that will consume this. Use the right code: 404 when something is missing, 201 when you create. Your front end will branch on these, so they must be truthful.
> 

### Exercise 8

Make your POST `/projects` return `201`. Then in GET `/projects/{project_id}`, raise a `404` with a helpful detail when the id is not one you recognise. Trigger both from `/docs` and read the status code each returns.

---

## Part 9 — Putting It Together

A small but complete projects API: list all, get one, and create. It stores data in a plain list for now — a real database comes later — but the shape of the code is exactly what you will keep.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
    title: str
    tech: str

# our "database" for now — just a list in memory
projects = [
    {"id": 1, "title": "Weather App", "tech": "React"},
    {"id": 2, "title": "Inventory", "tech": "FastAPI"},
]

@app.get("/projects")  # read the whole list
def list_projects():
    return projects

@app.get("/projects/{project_id}")  # read one
def get_project(project_id: int):
    for p in projects:
        if p["id"] == project_id:
            return p
    raise HTTPException(404, "Project not found")

@app.post("/projects", status_code=201)  # create one
def create_project(project: Project):
    new = {
        "id": len(projects) + 1,
        "title": project.title,
        "tech": project.tech,
    }
    projects.append(new)
    return new
```

> **Look at what each endpoint does:** `GET /projects` returns the list. `GET /projects/1` finds one or raises 404. `POST /projects` validates the body, adds it, and replies 201 with the new item. That is a real REST API — the same pattern scales to any resource, and the database later just replaces the list.
> 

> **This is exactly what your front end will call.** Your React app will `GET /projects`, receive this list, and map it into cards. When the user adds one, React will `POST` to this same endpoint. The two halves of the course meet here.
> 

### Exercise 9

Build this API. Then extend it: add a DELETE `/projects/{project_id}` route that removes a project or raises 404, and confirm the change by calling GET `/projects` again. Do it all from the `/docs` page.

---

## Part 10 — Quick Reference & Glossary

### Cheat sheet

| Task | Code |
| --- | --- |
| Create the app | `app = FastAPI()` |
| Run it | `fastapi dev main.py` |
| Interactive docs | `/docs` in the browser |
| GET route | `@app.get("/projects")` |
| POST route | `@app.post("/projects")` |
| Path parameter | `/projects/{id}`, `id: int` |
| Query parameter | arg not in path: `limit: int = 10` |
| Request body | a `BaseModel` arg: `project: Project` |
| Success code | `status_code=201` |
| Error | `raise HTTPException(404, "...")` |

### Common mistakes to avoid

| Mistake | Fix |
| --- | --- |
| Wrong indentation in Python | Indent consistently — it is the syntax |
| Committing `.venv/` or secrets | Add both to `.gitignore` |
| Verb in the path: `/getProjects` | Use nouns; let the method carry the action |
| Returning 200 with a "not found" body | Raise `HTTPException(404, ...)` |
| Skipping type hints | They power validation and the docs |
| No request model on a POST | Define a Pydantic model for the body |

### Glossary

| Term | Meaning |
| --- | --- |
| Back end | Code that runs on a server you control |
| API | The set of URLs the front end calls |
| Route / path operation | A path + method paired with a function |
| Decorator | The `@app.get(...)` line that wires a function to a route |
| Path parameter | A value inside the URL path, like an id |
| Query parameter | A value after `?`, for filtering or options |
| Pydantic model | A class describing the expected request data |
| Status code | A number saying what happened (200, 201, 404) |
| uvicorn | The server that runs your FastAPI app |
| Virtual environment | An isolated space for a project's packages |

### The bridge to your front end

You have now built both halves of a web application. Your FastAPI server exposes `/projects`; your React app will call it, map the results into components, and POST new data back. Everything from here — databases, authentication, testing, deployment — makes this API more capable, but the request–response shape you built today stays the same.

---

*End of guide · Web Systems and Technologies · College of Computer Studies*