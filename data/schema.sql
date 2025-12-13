CREATE TABLE Authors (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
birth_year INTEGER,
nationality TEXT
);
CREATE TABLE Books (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  isbn TEXT UNIQUE NOT NULL,
  year INTEGER,
  genre TEXT,
  copies INTEGER DEFAULT 1,
  author_id INTEGER,
  FOREIGN KEY(author_id) REFERENCES Authors(id)

);
CREATE TABLE Members (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  phone TEXT,
  membership_date TEXT,
  status TEXT
);
CREATE TABLE Loans (
  id INTEGER PRIMARY KEY,
  book_id INTEGER,
  member_id INTEGER,
loan_date TEXT,
due_date TEXT,
return_date TEXT,
status TEXT,
FOREIGN KEY(book_id) REFERENCES Books(id),
FOREIGN KEY(member_id) REFERENCES Members(id)
);

