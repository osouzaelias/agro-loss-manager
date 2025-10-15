def calcular_perda(potencial: float, colhido: float) -> tuple[float, float]:
    if potencial <= 0:
        return 0.0, 0.0

    perda_toneladas = potencial - colhido
    perda_percentual = (perda_toneladas / potencial) * 100

    return max(0, perda_toneladas), max(0, perda_percentual)