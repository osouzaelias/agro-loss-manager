from dataclasses import dataclass

@dataclass
class Colheita:
    id_talhao: str
    maquina: str
    operador: str
    toneladas_potenciais: float
    toneladas_colhidas: float
    id: int = None