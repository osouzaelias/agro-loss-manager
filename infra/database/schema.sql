CREATE TABLE IF NOT EXISTS colheitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_talhao TEXT NOT NULL,
    maquina TEXT NOT NULL,
    operador TEXT NOT NULL,
    toneladas_potenciais REAL NOT NULL,
    toneladas_colhidas REAL NOT NULL
);