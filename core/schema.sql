DROP TABLE IF EXISTS url;

CREATE TABLE url (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    clicked INTEGER
)