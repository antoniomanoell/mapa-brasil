"""`renda_pc` — renda domiciliar per capita média, real (ver DECISIONS.md).

Fase 1: só o segmento PNAD Contínua. O segmento PNAD 2001–2015 depende de microdados.
"""

from datetime import date

from ..escala import escala_quantil
from ..schema import Flag, Indicador, Ponto, Segmento, Subindicador
from ..sources import ibge_sidra
from ..validate import LIMIAR_CV_PADRAO, Regras, ultimo_ano_transcorrido

TABELA = 7533
VAR_VALOR = 10816
VAR_CV = 10817
CLASSE_TOTAL = "1019[49243]"
CASAS = 0


class RendaPc:
    id = "renda_pc"
    regras = Regras(
        faixa=(0, 20_000),
        limiar_variacao=0.15,
        metodologias={"pnadc": (2012, None)},
    )

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        inicio, fim_tabela = ibge_sidra.periodo(TABELA)
        fim = min(fim_tabela, ultimo_ano_transcorrido(hoje))
        dados, obtido_em = ibge_sidra.consultar(
            TABELA, [VAR_VALOR, VAR_CV], (inicio, fim), CLASSE_TOTAL
        )
        anos = list(range(inicio, fim + 1))

        valores: dict[str, dict[str, Ponto]] = {}
        for geo, serie in sorted(dados[VAR_VALOR].items()):
            for ano in anos:
                v = serie.get(ano)
                cv = dados[VAR_CV].get(geo, {}).get(ano)
                if v is None:
                    ponto = Ponto(v=None, lacuna="valor não publicado pelo IBGE")
                else:
                    flags = (
                        [Flag.BAIXA_PRECISAO] if cv is not None and cv > LIMIAR_CV_PADRAO else []
                    )
                    ponto = Ponto(v=v, cv=cv, flags=flags)
                valores.setdefault(geo, {})[str(ano)] = ponto

        seg = Segmento(
            id="pnadc",
            subindicador="principal",
            rotulo=f"PNAD Contínua ({inicio}–)",
            fonte="IBGE – PNAD Contínua anual (rendimento de todas as fontes)",
            fonte_url=ibge_sidra.url_tabela(TABELA),
            tabela=(
                f"SIDRA {TABELA}, variáveis {VAR_VALOR} (valor) e {VAR_CV} (CV), "
                f"classificação {CLASSE_TOTAL} (Total)"
            ),
            extraido_em=obtido_em,
            notas=(
                f"Valores em reais a preços médios de {fim}, deflacionados pelo IBGE com o IPCA. "
                "Segundo o IBGE, de 2020 a 2022 os dados vêm da 5ª visita da PNAD Contínua; nos "
                "demais anos, da 1ª. Ainda não há segmento da PNAD anual (2001–2015)."
            ),
            anos=anos,
            valores=valores,
        )
        return Indicador(
            id=self.id,
            nome="Renda domiciliar per capita média",
            tema="Renda",
            unidade="R$",
            unidade_detalhe=f"R$ de {fim} por mês (deflacionado pelo IPCA)",
            direcao="maior_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome="Renda domiciliar per capita")],
            segmentos=[seg],
            escalas={"principal": escala_quantil([seg], CASAS)},
            versao_pipeline=versao_pipeline,
        )
