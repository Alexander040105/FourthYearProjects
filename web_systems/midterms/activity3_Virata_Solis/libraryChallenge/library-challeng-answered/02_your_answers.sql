DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS loaned_books;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS book_copies;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS books;

CREATE TABLE members (
    member_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_name    TEXT NOT NULL,
    member_email   TEXT UNIQUE
);

CREATE TABLE books (
    book_id        INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  
    isbn           TEXT NOT NULL UNIQUE,                     
    title          TEXT NOT NULL,
    genre          TEXT
);

CREATE TABLE loaned_books (
    borrowed_id    INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  
    member_id      INT  NOT NULL REFERENCES members(member_id),
    book_id        INT  NOT NULL REFERENCES books(book_id),
    borrowed_on    DATE NOT NULL DEFAULT CURRENT_DATE,
    due_on         DATE NOT NULL,
    returned_on    DATE,                    -- NULL until the book comes back
    CHECK (due_on > borrowed_on),
    CHECK (returned_on IS NULL OR returned_on >= borrowed_on)
);


-- many to many relationship + separates the 'Cruz; Santos' style lists
CREATE TABLE authors (
    author_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name      TEXT NOT NULL,
    email     TEXT UNIQUE
);

CREATE TABLE book_authors (
    book_id   INT NOT NULL REFERENCES books(book_id),
    author_id INT NOT NULL REFERENCES authors(author_id),
    PRIMARY KEY (book_id, author_id) 
);



CREATE TABLE book_copies (
    copy_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    book_id INT  NOT NULL REFERENCES books(book_id),
    status  TEXT NOT NULL DEFAULT 'available'
            CHECK (status IN ('available', 'on_loan', 'lost', 'maintenance'))
);

ALTER TABLE loaned_books
    ADD COLUMN copy_id INT REFERENCES book_copies(copy_id);

CREATE TABLE reservations (
    reservation_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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


INSERT INTO members (member_name, member_email) VALUES
    ('Ana Cruz',    'ana@u.edu'),
    ('Ben Lim',     'ben@u.edu'),
    ('Cy Dela Cruz','cy@u.edu'),
    ('Dara Yu',     'dara@u.edu');      -- made just for Q9 borrower

INSERT INTO books (isbn, title, genre) VALUES
    ('978-1', 'Web Systems',        'Tech'),
    ('978-2', 'Databases',          'Tech'),
    ('978-3', 'Networks',           'Tech'),
    ('978-4', 'Operating Systems',  'Tech'),
    ('978-5', 'Clean Architecture', 'Tech');  -- made just for never borrowed Q10

INSERT INTO authors (name, email) VALUES
    ('Cruz',   'cruz@p.edu'),
    ('Santos', 'santos@p.edu'),
    ('Reyes',  'reyes@p.edu'),
    ('Tan',    'tan@p.edu');

INSERT INTO book_authors (book_id, author_id) VALUES
    (1, 1), (1, 2), (2, 3), (3, 3), (4, 3), (5, 4);

INSERT INTO book_copies (book_id, status) VALUES
    (1, 'on_loan'),    (1, 'available'),  (2, 'on_loan'),    (2, 'on_loan'),
    (3, 'on_loan'),    (3, 'on_loan'),    (4, 'on_loan'),    (5, 'available');

-- loans: the five inherited rows, plus four active loans for Dara.
-- (sample due dates are in June 2026, so unreturned ones ARE overdue.)
INSERT INTO loaned_books (member_id, book_id, copy_id, borrowed_on, due_on, returned_on) VALUES
    (1, 1, 1, '2026-06-01', '2026-06-15', '2026-06-10'),  
    (1, 2, 3, '2026-06-03', '2026-06-17', '2026-06-17'),  
    (2, 1, 2, '2026-06-05', '2026-06-19', '2026-06-18'),  
    (2, 3, 5, '2026-06-08', '2026-06-22', NULL),          -- overdue
    (3, 2, 4, '2026-06-09', '2026-06-23', NULL),          -- overdue
    (4, 1, 1, '2026-09-10', '2026-09-24', NULL),          
    (4, 2, 3, '2026-09-10', '2026-09-24', NULL),          
    (4, 3, 6, '2026-09-10', '2026-09-24', NULL),          
    (4, 4, 7, '2026-09-10', '2026-09-24', NULL);          

-- every copy of 'Networks' is out -> Ana queues for the title
INSERT INTO reservations (book_id, member_id, reserved_on) VALUES
    (3, 1, '2026-09-16 09:30');


-- ---- PART C · QUERY -------------------------------------------------
-- (run these against YOUR normalized tables above)

-- Q8  Every loan: member name, book title, borrowed date (3-table join)
-- m = members, b = books, l = loaned_books
SELECT m.member_name, b.title, l.borrowed_on 
FROM loaned_books AS l LEFT JOIN members AS m 
ON l.member_id = m.member_id 
LEFT JOIN books AS b ON l.book_id = b.book_id;

-- Q9  Members with more than 3 books currently on loan (GROUP BY + HAVING)
SELECT m.member_name FROM members AS m 
INNER JOIN loaned_books AS l
ON m.member_id = l.member_id
WHERE l.returned_on IS NULL
GROUP BY m.member_id, m.member_name HAVING COUNT(borrowed_id) > 3;


-- Q10 Titles of books never borrowed (subquery)
SELECT b.title
FROM books b
WHERE NOT EXISTS (
    SELECT 1
    FROM loaned_books AS l
    WHERE l.book_id = b.book_id
);


-- Q11 Books overdue right now, with the member who has them (CURRENT_DATE)
-- title, member name, returned_on is null, CURRENT_DATE
SELECT b.title, m.member_name FROM loaned_books AS l 
LEFT JOIN members AS m 
ON l.member_id = m.member_id 
LEFT JOIN books AS b ON l.book_id = b.book_id
WHERE l.returned_on IS NULL AND CURRENT_DATE > l.due_on;

-- Q12 (no SQL) In a comment, say what the given query returns and why.
