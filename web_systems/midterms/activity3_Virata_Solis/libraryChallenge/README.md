# Week 9 Challenge — The Campus Library (Student Files)

These files go with the **Database Design Challenge** handout. You will diagnose
a flawed database, redesign it, and query your redesign.

## What's here

- **`01_flawed_database.sql`** — the single broken table you inherited
  (`circulation`). Load it, look at it, and use it for **Part A (Analyze)**.
  Do not edit it to "fix" it — that is what Part B is for.
- **`02_your_answers.sql`** — your workspace. Write your redesign (Part B) and
  your queries (Part C) here. This is the file you submit.

## What you need

- **PostgreSQL 14+** and its `psql` command line (or any client, e.g. pgAdmin).

## How to run it

```bash
# 1. create a database for this challenge
createdb library_challenge

# 2. load the flawed table
psql -d library_challenge -f 01_flawed_database.sql

# 3. open a session and look around
psql -d library_challenge
```

Then, inside `psql`:

```sql
SELECT * FROM circulation;
```

## Your job

1. **Part A — Analyze.** Study `circulation`. Find its functional dependencies,
   its anomalies, and the normal form it is stuck in.
2. **Part B — Create.** In `02_your_answers.sql`, write the normalized schema,
   the many-to-many author design, and the copies/reservations extension. Run
   your `CREATE TABLE` statements to confirm they work.
3. **Part C — Query.** Still in `02_your_answers.sql`, write and run the five
   queries against **your** tables. You will need to add a little sample data of
   your own so the queries return rows.

Everything you need to answer is on the handout. Reason it through — most
questions have more than one defensible answer.
