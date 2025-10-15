from application.interfaces.colheita_repository import ColheitaRepository


class ListarColheitas:
    def __init__(self, repository: ColheitaRepository):
        self.repository = repository

    def execute(self):
        return self.repository.listar_todos()