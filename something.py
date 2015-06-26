CREATE TABLE IF NOT EXISTS entries (
    id serial PRIMARY KEY,
    title VARCHAR (128) NOT NULL,
    text TEXT NOT NULL,
    created TIMESTAMP NOT NULL
)