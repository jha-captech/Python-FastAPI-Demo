-- create authors table
CREATE TABLE authors
(
    id          SERIAL PRIMARY KEY,
    first_name  VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    last_name   VARCHAR(255) NOT NULL
);

-- seed authors table
INSERT INTO authors (first_name, middle_name, last_name)
VALUES ('John', 'Ronald Reuel', 'Tolkien'),
       ('George', '', 'Orwell'),
       ('J.K.', '', 'Rowling'),
       ('Stephen', '', 'King'),
       ('Agatha', '', 'Christie');

-- create publishers table
CREATE TABLE publishers
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- seed publishers table
INSERT INTO publishers (name)
VALUES ('HarperCollins'),
       ('Penguin Random House'),
       ('Bloomsbury'),
       ('Houghton Mifflin Harcourt'),
       ('William Morrow');

-- create books table
CREATE TABLE books
(
    id           SERIAL PRIMARY KEY,
    title        VARCHAR(255) NOT NULL,
    author_id    INT          NOT NULL,
    publisher_id INT          NOT NULL,
    publication  DATE         NOT NULL,
    pages        INT          NOT NULL,
    language     VARCHAR(255) NOT NULL,
    isbn         VARCHAR(255) NOT NULL,
    description  TEXT
);

-- seed books table
INSERT INTO books (title, author_id, publisher_id, publication, pages, language, isbn, description)
VALUES ('The Lord of the Rings', 1, 1, '1954-07-29', 1178, 'English', '9780618640157',
        'The Lord of the Rings is an epic high-fantasy novel written by English author and scholar J. R. R. Tolkien.'),
       ('1984', 2, 2, '1949-06-08', 328, 'English', '9780451524935',
        '1984 is a dystopian social science fiction novel by English novelist George Orwell.'),
       ('Harry Potter and the Philosopher''s Stone', 3, 3, '1997-06-26', 223, 'English', '9780747532743',
        'Harry Potter and the Philosopher''s Stone is a fantasy novel written by British author J. K. Rowling.'),
       ('The Shining', 4, 4, '1977-01-28', 447, 'English', '9780385121675',
        'The Shining is a horror novel by American author Stephen King.')