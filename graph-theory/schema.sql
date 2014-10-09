CREATE TABLE IF NOT EXISTS vertices (
       id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS edges (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       first_id INTEGER REFERENCES vertices(id),
       second_id INTEGER REFERENCES vertices(id),
       UNIQUE(first_id, second_id)
);
CREATE INDEX edges_first_id_idx ON edges(first_id);
CREATE INDEX edges_second_id_idx ON edges(second_id);
