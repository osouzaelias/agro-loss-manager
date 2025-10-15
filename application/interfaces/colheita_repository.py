from abc import ABC, abstractmethod
from typing import List
from domain.entities.colheita import Colheita

class ColheitaRepository(ABC):
    @abstractmethod
    def salvar(self, colheita: Colheita) -> Colheita:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Colheita]:
        pass