import sqlite3
from typing import List
from domain.entities.colheita import Colheita
from application.interfaces.colheita_repository import ColheitaRepository
from infra.database.database import get_connection


class SQLiteColheitaRepository(ColheitaRepository):
    def salvar(self, colheita: Colheita) -> Colheita:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO colheitas (id_talhao, maquina, operador, toneladas_potenciais, toneladas_colhidas)
            VALUES (?, ?, ?, ?, ?)
            """,
            (colheita.id_talhao, colheita.maquina, colheita.operador, colheita.toneladas_potenciais,
             colheita.toneladas_colhidas)
        )
        colheita.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return colheita

    def listar_todos(self) -> List[Colheita]:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM colheitas ORDER BY id")
        rows = cursor.fetchall()
        conn.close()

        return [Colheita(**row) for row in rows]