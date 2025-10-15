from domain.entities.colheita import Colheita
from application.interfaces.colheita_repository import ColheitaRepository


class CadastrarColheita:
    def __init__(self, repository: ColheitaRepository):
        self.repository = repository

    def execute(self, dados_colheita: dict) -> Colheita:
        nova_colheita = Colheita(**dados_colheita)
        return self.repository.salvar(nova_colheita)