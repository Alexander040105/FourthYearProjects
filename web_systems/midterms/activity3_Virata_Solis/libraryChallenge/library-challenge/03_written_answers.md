# Database Design Challenge — Written Answers (Parts A & D)

*Companion to `02_your_answers.sql`, which holds all executable SQL for
Parts B and C.*

---

## Part A · Analyze — Diagnosing `circulation`

### Q1 — Functional dependencies

Working from the sample rows (key = `(member_id, isbn)`):

| FD | What it says |
|---|---|
| `(member_id, isbn) → borrowed_on, due_on` | A specific loan determines when it was borrowed and when it is due. |
| `member_id → member_name, member_email` | The member's identity determines their name and email. |
| `isbn → title, genre, authors` | The book determines its own facts. |
| `authors → author_emails` | An author determines their email — the email is not a fact about the *loan*. |
| `member_email → member_id` (secondary) | Email is a plausible alternate identifier for a member — worth noting as a candidate key. |

### Q2 — Classification

| FD | Class | Why |
|---|---|---|
| `(member_id, isbn) → borrowed_on, due_on` | **Full** | Needs the whole key; neither member nor book alone fixes the dates. |
| `member_id → member_name, member_email` | **Partial** | Determined by part of the key only. |
| `isbn → title, genre, authors` | **Partial** | Determined by part of the key only. |
| `authors → author_emails` | **Transitive** | Chain: `(member_id, isbn) → isbn → authors → author_emails`. The email reaches the key through two hops. |

### Q3 — The three anomalies, with evidence

| Anomaly | Concrete example from the data |
|---|---|
| **Update** | `ana@u.edu` is stored on **two** rows (member 1, isbn 978-1 and 978-2). If Ana changes her email and only one row is updated, the database holds two different emails for the same person. Same hazard for `'Web Systems'`, repeated on the rows for members 1 and 2. |
| **Insertion** | A new title that nobody has borrowed yet cannot be stored — a row requires a `member_id`, and `NULL` would break the key. Likewise a newly registered member with no loans has nowhere to exist. |
| **Deletion** | The row `(3, 'Cy Dela Cruz', …, 978-2, …)` is the **only** row for member 3 — deleting that loan erases Cy from the library entirely. Similarly `(2, 'Ben Lim', …, 978-3, …)` is the only row mentioning *Networks*; deleting it makes the book cease to exist. |

### Q4 — Highest normal form

**At best 1NF** — and only once `authors` / `author_emails` are split into atomic values, since `'Cruz; Santos'` is not atomic.

It fails **2NF**: the rule is that every non-key attribute must depend on the *whole* key, but `member_name` depends only on `member_id` and `title` depends only on `isbn` — both are partial dependencies on `(member_id, isbn)`.

(It also would fail 3NF on the `authors → author_emails` transitive chain, but 2NF is already the wall.)

---

## Part B · Create — Q5 stepwise decomposition

*(The `CREATE TABLE` statements live in `02_your_answers.sql`; here are the
intermediate table sets and what each step removed.)*

**→ 1NF** — removed the **multivalued attribute**: explode `'Cruz; Santos'`
into one row per author per loan. Every cell is now atomic, but redundancy
is unchanged — the table just got taller.

```
circulation_1nf(member_id, member_name, member_email,
                isbn, title, genre, author, author_email,
                borrowed_on, due_on)
```

**→ 2NF** — removed the **partial dependencies**
(`member_id → member_name, member_email` and `isbn → title, genre`):

```
members(member_id PK, member_name, member_email)
books_authors(isbn, title, genre, author, author_email)   -- still tall
loans(member_id FK, isbn FK, borrowed_on, due_on)
```

**→ 3NF** — removed the **transitive dependency**
(`isbn → authors → author_emails`): author emails move out of the book rows
into their own table, linked through the junction:

```
members(member_id PK, member_name, member_email UNIQUE)
books(book_id PK, isbn UNIQUE, title, genre)
authors(author_id PK, name, email UNIQUE)
book_authors(book_id FK, author_id FK, PK(book_id, author_id))
loans(loan_id PK, member_id FK, book_id FK,
      borrowed_on, due_on, returned_on)
```

No non-key attribute now depends on anything but its table's whole key —
that is the definition of 3NF.

### Q6 — junction-table key (higher-order answer)

`book_authors` uses the **composite primary key `(book_id, author_id)`**.
A standalone `SERIAL id` cannot prevent duplicate links: two identical
`(book, author)` pairs would simply receive different surrogate ids and
both insert cleanly. The pair itself *is* the thing that must be unique,
so the pair must be the key. (A surrogate is only safe if you also declare
`UNIQUE(book_id, author_id)` — which is the composite key with extra steps.)

### Q7 — assumptions behind the copies/reservations design

Hidden decisions in the librarian's one sentence:

1. **"Several physical copies"** → a loan must bind to a *copy*, not a
   title — hence `book_copies` and `loans.copy_id`. We keep `loans.book_id`
   too so Part C stays a clean three-table join (noted as a deliberate
   trade-off; the strict alternative is reaching the title through
   `book_copies` only).
2. **"Reserve a title… in the order they asked"** → reservations are per
   *title*, and queue order is **derived** from `reserved_on` rather than
   stored as a position integer — a stored position invites renumbering
   anomalies whenever anyone cancels. The partial unique index
   `one_waiting_reservation_per_title` stops a member double-queueing.

---

## Part D · Evaluate — Defended decisions

### Q13 — The `loan_report` denormalized table

- **Advantage:** dashboard reads need no joins — one table scan, simple
  SQL, predictable latency regardless of how many members/books exist.
- **Cost:** it reintroduces exactly the anomalies we just removed —
  renaming a member or retitling a book leaves stale copies in every
  report row unless something keeps them in sync.

**Recommendation: against.** At campus-library scale, joins on indexed
primary keys are cheap; the duplication buys nothing measurable and costs
a sync mechanism. If the dashboard genuinely must avoid joins, use a
`VIEW` (no stored duplication) or a `MATERIALIZED VIEW` refreshed on a
schedule — the read benefit without hand-maintained copies. **Reversal
condition:** I would accept `loan_report` only if reads dominated *and*
profiling showed the join path was the actual bottleneck.

### Q14 — Clickstream: SQL or NoSQL?

**NoSQL** (an append-only event store — Cassandra/ClickHouse-style).
Millions of events a day, loss-tolerant, schema-flexible: that is a
**BASE** workload — Basically Available, Soft state, Eventually
consistent. Paying **ACID** prices (locking, immediate consistency,
durability ceremony) per page-view buys correctness guarantees nobody
needs.

**The opposite choice is clearly correct for loans and reservations** —
two members must never hold the same physical copy, and a reservation
queue must not reorder itself. That data needs ACID transactions: keep it
in PostgreSQL.

### Q15 — When to deliberately break 3NF, and the safeguard

**Condition:** a read-heavy, write-rare path where *measured* evidence
(profiling, not suspicion) shows the join or aggregation is the
bottleneck — e.g. a "top borrowed titles" widget recomputed per request.

**Safeguard:** never let humans maintain the duplicate. Keep the
normalized tables as the single source of truth and derive the copy
mechanically — a `MATERIALIZED VIEW` with scheduled refresh, or a
trigger-maintained summary column — so the duplicated data cannot
silently drift from the real data.
