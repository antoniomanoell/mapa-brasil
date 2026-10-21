"""Taxas anuais da PNAD Contínua publicadas no SIDRA: `desocupacao` e `informalidade`.

O IBGE publica a taxa anual em tabela própria (é o número que divulga como "taxa anual").
Ela não é a média simples das taxas trimestrais e não é recalculada aqui.
"""

from datetime import date

from ..escala import escala_quantil
from ..schema import Flag, Indicador, Ponto, Segmento, Subindicador
from ..sources import ibge_sidra
from ..validate import LIMIAR_CV_PADRAO, Regras, ultimo_ano_transcorrido

CASAS = 1


class TaxaPnadcAnual:
    def __init__(
        self,
        id_: str,
        tabela: int,
        var_valor: int,
        var_cv: int,
        nome: str,
        tema: str,
        unidade_detalhe: str,
        notas: str,
        regras: Regras,
    ) -> None:
        self.id = id_
        self.tabela = tabela
        self.var_valor = var_valor
        self.var_cv = var_cv
        self.nome = nome
        self.tema = tema
        self.unidade_detalhe = unidade_detalhe
        self.notas = notas
        self.regras = regras

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        inicio, fim_tabela = ibge_sidra.periodo(self.tabela)
        fim = min(fim_tabela, ultimo_ano_transcorrido(hoje))
        dados, obtido_em = ibge_sidra.consultar(
            self.tabela, [self.var_valor, self.var_cv], (inicio, fim)
        )
        anos = list(range(inicio, fim + 1))
        valores: dict[str, dict[str, Ponto]] = {}
        for geo, serie in sorted(dados[self.var_valor].items()):
            for ano in anos:
                v = serie.get(ano)
                cv = dados[self.var_cv].get(geo, {}).get(ano)
                if v is None:
                    ponto = Ponto(v=None, lacuna="valor não publicado pelo IBGE")
                else:
                    alto = cv is not None and cv > LIMIAR_CV_PADRAO
                    ponto = Ponto(v=v, cv=cv, flags=[Flag.BAIXA_PRECISAO] if alto else [])
                valores.setdefault(geo, {})[str(ano)] = ponto

        seg = Segmento(
            id="pnadc",
            subindicador="principal",
            rotulo=f"PNAD Contínua ({inicio}–)",
            fonte="IBGE – PNAD Contínua anual (mercado de trabalho)",
            fonte_url=ibge_sidra.url_tabela(self.tabela),
            tabela=f"SIDRA {self.tabela}, variáveis {self.var_valor} (taxa) e {self.var_cv} (CV)",
            extraido_em=obtido_em,
            notas=self.notas,
            anos=anos,
            valores=valores,
        )
        return Indicador(
            id=self.id,
            nome=self.nome,
            tema=self.tema,
            unidade="%",
            unidade_detalhe=self.unidade_detalhe,
            direcao="menor_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome=self.nome)],
            segmentos=[seg],
            escalas={"principal": escala_quantil([seg], CASAS)},
            versao_pipeline=versao_pipeline,
        )


def desocupacao() -> TaxaPnadcAnual:
    return TaxaPnadcAnual(
        "desocupacao",
        4562,
        4099,
        4103,
        "Taxa de desocupação",
        "Trabalho",
        "% da força de trabalho (14 anos ou mais) desocupada",
        (
            "Taxa anual publicada pelo IBGE. Não há série anterior a 2012: a PNAD anual usava "
            "outro conceito de desocupação, e as séries não são comparáveis."
        ),
        Regras(faixa=(0, 100), limiar_variacao=0.35, metodologias={"pnadc": (2012, None)}),
    )


def informalidade() -> TaxaPnadcAnual:
    return TaxaPnadcAnual(
        "informalidade",
        4708,
        12466,
        12467,
        "Taxa de informalidade",
        "Trabalho",
        "% das pessoas ocupadas (14 anos ou mais) em trabalho informal, pela definição do IBGE",
        "Taxa anual publicada pelo IBGE. A série começa em 2016, primeiro ano da tabela no SIDRA.",
        Regras(faixa=(0, 100), limiar_variacao=0.15, metodologias={"pnadc": (2016, None)}),
    )
