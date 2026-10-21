"""`pib_pc` — PIB per capita real (ver DECISIONS.md).

PIB real a preços do último ano = PIB corrente do último ano × volume encadeado do ano ÷ volume do
último ano (Contas Regionais, referência 2010). Não usa IPCA (PROJECT.md, 4.1). Divide pela
população única da seção 4.2.
"""

from datetime import date

from ..escala import escala_quantil
from ..population import FONTE as FONTE_POP
from ..population import populacao
from ..raw_manual import carregar_manifest
from ..schema import Indicador, Ponto, Segmento, Subindicador
from ..sources import ibge_contas_regionais as cr
from ..validate import Auxiliares, Regras, ultimo_ano_transcorrido

CASAS = 0
# Conferência indireta: crescimento real acumulado do PIB, primeiro → último ano (%), que o IBGE
# divulga junto com as Contas Regionais.
AUX_ACUMULADO = "cr_volume_acumulado"


class PibPc:
    id = "pib_pc"
    regras = Regras(
        faixa=(1_000, 500_000),
        limiar_variacao=0.12,
        metodologias={"cr2010": (2002, None)},
    )

    def __init__(self) -> None:
        self.auxiliares: Auxiliares = {}

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        dados = cr.especiais()
        anos_tabela = sorted(dados.volume["BR"])
        anos = [a for a in anos_tabela if a <= ultimo_ano_transcorrido(hoje)]
        base = anos[-1]
        pop = populacao(base)
        valores: dict[str, dict[str, Ponto]] = {}
        for geo in sorted(dados.volume):
            corrente_base = dados.pib_corrente[geo][base]
            vol = dados.volume[geo]
            for ano in anos:
                real = corrente_base * vol[ano] / vol[base]  # R$ milhões de `base`
                valores.setdefault(geo, {})[str(ano)] = Ponto(
                    v=round(real * 1e6 / pop[geo][ano], 2), n=round(real, 1)
                )
            self.auxiliares[(AUX_ACUMULADO, "principal", "cr2010", geo, base)] = round(
                (vol[base] / vol[anos[0]] - 1) * 100, 2
            )

        seg = Segmento(
            id="cr2010",
            subindicador="principal",
            rotulo=f"Contas Regionais, ref. 2010 ({anos[0]}–{base})",
            fonte=f"IBGE – Contas Regionais do Brasil; população: {FONTE_POP}",
            fonte_url=cr.URL,
            tabela=(
                "Especiais_2002_2023_xls.zip — tab01 (PIB corrente) e tab03 (série encadeada do "
                "volume do PIB)"
            ),
            extraido_em=carregar_manifest()[cr.ARQUIVO].baixado_em,
            notas=(
                f"PIB real a preços de {base}: o PIB corrente de {base} é levado aos outros anos "
                "pela série encadeada do volume do PIB, sem índice de preços ao consumidor. Série "
                "de referência 2010 das Contas Regionais, não emendada com as anteriores. A "
                "população é a das Projeções do IBGE (Revisão 2024), a mesma de todo o site e "
                "das Contas Nacionais (Brasil 2023: R$ 51.694). A divulgação das Contas Regionais "
                "usa a população recenseada e por isso traz per capita de 3% a 8% maiores "
                "(Brasil 2023: R$ 53.887)."
            ),
            anos=anos,
            valores=valores,
        )
        return Indicador(
            id=self.id,
            nome="PIB per capita",
            tema="Renda",
            unidade="R$",
            unidade_detalhe=f"R$ de {base} por habitante, por ano (volume encadeado)",
            direcao="maior_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome="PIB per capita")],
            segmentos=[seg],
            escalas={"principal": escala_quantil([seg], CASAS)},
            versao_pipeline=versao_pipeline,
        )
