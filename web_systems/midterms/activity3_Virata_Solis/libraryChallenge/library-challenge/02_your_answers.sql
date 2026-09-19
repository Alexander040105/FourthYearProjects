-- =====================================================================
--  Week 9 Challenge — YOUR WORKSPACE
--  Write your redesign (Part B) and your queries (Part C) here.
--  Keep each answer under its heading. This file is what you submit.
-- =====================================================================

-- ---- PART B · CREATE ------------------------------------------------

-- Q5  Normalized schema (to 3NF). Write your CREATE TABLE statements.
--
-- Steps taken (full write-up in 03_written_answers.md):
--   1NF: split 'Cruz; Santos' style lists into atomic values (one row
--        per author per loan) -> removes the multivalued attribute.
--   2NF: split out partial dependencies
--        member_id -> member_name, member_email   => members
--        isbn      -> title, genre                => books
--        leaving (member_id, isbn) -> borrowed_on, due_on => loans
--   3NF: split out the transitive dependency
--        isbn -> authors -> author_emails
--        => authors + book_authors (see Q6).

CREATE TABLE members (
    member_id    SERIAL PRIMARY KEY,
    member_name  TEXT NOT NULL,
    member_email TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,          -- surrogate PK (Q12 joins on book_id)
    isbn    TEXT NOT NULL UNIQUE,        -- natural key kept unique
    title   TEXT NOT NULL,
    genre   TEXT
);

CREATE TABLE loans (
    loan_id     SERIAL PRIMARY KEY,      -- a member may re-borrow a title,
                                         -- so (member_id, book_id) alone is
                                         -- not a safe key anymore
    member_id   INT  NOT NULL REFERENCES members(member_id),
    book_id     INT  NOT NULL REFERENCES books(book_id),
    borrowed_on DATE NOT NULL DEFAULT CURRENT_DATE,
    due_on      DATE NOT NULL,
    returned_on DATE,                    -- NULL until the book comes back
    CHECK (due_on > borrowed_on),
    CHECK (returned_on IS NULL OR returned_on >= borrowed_on)
);


-- Q6  Many-to-many: books and authors, with a junction table.

CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    name      TEXT NOT NULL,
    email     TEXT UNIQUE
);

CREATE TABLE book_authors (
    book_id   INT NOT NULL REFERENCES books(book_id),
    author_id INT NOT NULL REFERENCES authors(author_id),
    PRIMARY KEY (book_id, author_id)     -- composite PK: the same author can
                                         -- never be linked to the same book
                                         -- twice. A lone SERIAL id could not
                                         -- stop that, because each duplicate
                                         -- row would just get a new id.
);


-- Q7  Extension: multiple physical copies + reservation queue.
--
-- Assumptions:
--   * A loan is of a specific PHYSICAL COPY, not just the title.
--   * Reservations are per TITLE; the queue is first-come-first-served
--     (order is derived from reserved_on — no stored position to renumber).
--   * A member may hold at most one WAITING reservation per title.
--   * loans keeps book_id (the title that was loaned) so Part C queries
--     stay simple; copy_id records which physical item went out. In a
--     stricter design you could drop loans.book_id and reach the title
--     through book_copies — we keep both for query clarity and note that
--     copy_id -> book_id is guaranteed by the FK chain.

CREATE TABLE book_copies (
    copy_id SERIAL PRIMARY KEY,
    book_id INT  NOT NULL REFERENCES books(book_id),
    status  TEXT NOT NULL DEFAULT 'available'
            CHECK (status IN ('available', 'on_loan', 'lost', 'maintenance'))
);

ALTER TABLE loans
    ADD COLUMN copy_id INT REFERENCES book_copies(copy_id);

CREATE TABLE reservations (
    reservation_id SERIAL PRIMARY KEY,
    book_id        INT NOT NULL REFERENCES books(book_id),
    member_id      INT NOT NULL REFERENCES members(member_id),
    reserved_on    TIMESTAMPTZ NOT NULL DEFAULT now(),  -- queue position
    status         TEXT NOT NULL DEFAULT 'waiting'
                   CHECK (status IN ('waiting', 'fulfilled', 'cancelled'))
);

-- at most one waiting reservation per (title, member)
CREATE UNIQUE INDEX one_waiting_reservation_per_title
    ON reservations (book_id, member_id)
    WHERE status = 'waiting';


-- ---- SAMPLE DATA ----------------------------------------------------
-- Reproduces the inherited rows plus enough extra data so every Part C
-- query returns something meaningful.

INSERT INTO members (member_id, member_name, member_email) VALUES
    (1, 'Ana Cruz',    'ana@u.edu'),
    (2, 'Ben Lim',     'ben@u.edu'),
    (3, 'Cy Dela Cruz','cy@u.edu'),
    (4, 'Dara Yu',     'dara@u.edu');      -- heavy borrower (for Q9)

INSERT INTO books (book_id, isbn, title, genre) VALUES
    (1, '978-1', 'Web Systems',        'Tech'),
    (2, '978-2', 'Databases',          'Tech'),
    (3, '978-3', 'Networks',           'Tech'),
    (4, '978-4', 'Operating Systems',  'Tech'),
    (5, '978-5', 'Clean Architecture', 'Tech');  -- never borrowed (for Q10)

INSERT INTO authors (author_id, name, email) VALUES
    (1, 'Cruz',   'cruz@p.edu'),
    (2, 'Santos', 'santos@p.edu'),
    (3, 'Reyes',  'reyes@p.edu'),
    (4, 'Tan',    'tan@p.edu');

INSERT INTO book_authors (book_id, author_id) VALUES (1, 1), (1, 2), (2, 3), (3, 3),(4, 3), (5, 4);                

INSERT INTO book_copies (copy_id, book_id, status) VALUES
    (1, 1, 'on_loan'),    (2, 1, 'available'),  (3, 2, 'on_loan'),    (4, 2, 'on_loan'),    
    (5, 3, 'on_loan'),    (6, 3, 'on_loan'),   (7, 4, 'on_loan'), (8, 5, 'available');

-- loans: the five inherited rows, plus four active loans for Dara.
-- (sample due dates are in June 2026, so unreturned ones ARE overdue.)
INSERT INTO loans (member_id, book_id, copy_id, borrowed_on, due_on, returned_on) VALUES
    (1, 1, 1, '2026-06-01', '2026-06-15', '2026-06-10'),  -- returned
    (1, 2, 3, '2026-06-03', '2026-06-17', '2026-06-17'),  -- returned
    (2, 1, 2, '2026-06-05', '2026-06-19', '2026-06-18'),  -- returned
    (2, 3, 5, '2026-06-08', '2026-06-22', NULL),          -- OVERDUE
    (3, 2, 4, '2026-06-09', '2026-06-23', NULL),          -- OVERDUE
    (4, 1, 1, '2026-09-10', '2026-09-24', NULL),          -- active
    (4, 2, 3, '2026-09-10', '2026-09-24', NULL),          -- active
    (4, 3, 6, '2026-09-10', '2026-09-24', NULL),          -- active
    (4, 4, 7, '2026-09-10', '2026-09-24', NULL);          -- active -> Dara has 4

-- every copy of 'Networks' is out -> Ana queues for the title
INSERT INTO reservations (book_id, member_id, reserved_on) VALUES (3, 1, '2026-09-16 09:30');

-- explicit ids above leave the SERIAL sequences behind; resync them so
-- later inserts don't collide with seeded rows
SELECT setval('members_member_id_seq',       (SELECT MAX(member_id)  FROM members));
SELECT setval('books_book_id_seq',           (SELECT MAX(book_id)    FROM books));
SELECT setval('authors_author_id_seq',       (SELECT MAX(author_id)  FROM authors));
SELECT setval('book_copies_copy_id_seq',     (SELECT MAX(copy_id)    FROM book_copies));
SELECT setval('loans_loan_id_seq',           (SELECT MAX(loan_id)    FROM loans));
SELECT setval('reservations_reservation_id_seq', (SELECT MAX(reservation_id) FROM reservations));


-- ---- PART C · QUERY -------------------------------------------------
-- (run these against YOUR normalized tables above)

-- Q8  Every loan: member name, book title, borrowed date (3-table join)

SELECT m.member_name, b.title, l.borrowed_on
FROM loans l
JOIN members m ON m.member_id = l.member_id
JOIN books   b ON b.book_id   = l.book_id
ORDER BY l.borrowed_on;


-- Q9  Members with more than 3 books currently on loan (GROUP BY + HAVING)
--     WHERE filters rows BEFORE grouping, so it can never see COUNT(*) —
--     the count only exists after GROUP BY. That is what HAVING is for.

SELECT member_id, COUNT(*) AS books_on_loan
FROM loans
WHERE returned_on IS NULL          -- rows first: only active loans
GROUP BY member_id
HAVING COUNT(*) > 3;               -- then filter the groups


-- Q10 Titles of books never borrowed (subquery)
--     NOT EXISTS chosen over NOT IN: it is NULL-safe. If the subquery
--     ever produced a NULL book_id, NOT IN would silently return no rows.

SELECT b.title
FROM books b
WHERE NOT EXISTS (
    SELECT 1
    FROM loans l
    WHERE l.book_id = b.book_id
);


-- Q11 Books overdue right now, with the member who has them (CURRENT_DATE)

SELECT b.title, m.member_name, l.due_on
FROM loans l
JOIN books   b ON b.book_id   = l.book_id
JOIN members m ON m.member_id = l.member_id
WHERE l.returned_on IS NULL
  AND l.due_on < CURRENT_DATE
ORDER BY l.due_on;


-- Q12 (no SQL) In a comment, say what the given query returns and why.
--
-- The query
--     SELECT m.member_name, COUNT(l.book_id) AS total
--     FROM members m LEFT JOIN loans l ON l.member_id = m.member_id
--     GROUP BY m.member_name ORDER BY total DESC;
-- asks: "how many loans does each member have?" It returns one row per
-- member with their loan count, highest first. On our data: Dara Yu 4,
-- Ana Cruz 2, Ben Lim 2, Cy Dela Cruz 1 — and any member with no loans
-- still appears with total 0, because the LEFT JOIN keeps them and
-- COUNT(l.book_id) counts only non-NULL matches.
-- A single missing word changes it: drop LEFT (a plain JOIN is inner)
-- and every zero-loan member disappears from the result.
