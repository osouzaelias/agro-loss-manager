from typing import List
from domain.entities.colheita import Colheita
from domain.services.calculo_perda_service import calcular_perda


class GerarRelatorioTXT:
    def execute(self, registros: List[Colheita]):
        if not registros:
            return

        total_perda_geral = 0
        total_potencial_geral = 0

        with open('relatorio_perdas.txt', 'w', encoding='utf-8') as f:
            f.write("--- Relatório de Análise de Perdas na Colheita ---\n\n")

            for reg in registros:
                perda_ton, perda_pct = calcular_perda(reg.toneladas_potenciais, reg.toneladas_colhidas)
                total_perda_geral += perda_ton
                total_potencial_geral += reg.toneladas_potenciais

                f.write(f"Registro do Talhão: {reg.id_talhao}\n")
                f.write(f"  - Máquina/Operador: {reg.maquina} / {reg.operador}\n")
                f.write(f"  - Potencial: {reg.toneladas_potenciais:.2f}t | Colhido: {reg.toneladas_colhidas:.2f}t\n")
                f.write(f"  - Perda: {perda_ton:.2f}t ({perda_pct:.2f}%)\n")
                f.write("-" * 30 + "\n")

            if total_potencial_geral > 0:
                media_geral_perda = (total_perda_geral / total_potencial_geral) * 100
                f.write("\n--- Resumo Geral ---\n")
                f.write(f"  - Total de Toneladas Perdidas: {total_perda_geral:.2f}t\n")
                f.write(f"  - Média de Perda Consolidada: {media_geral_perda:.2f}%\n")