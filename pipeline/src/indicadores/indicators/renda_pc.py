"""`renda_pc` — renda domiciliar per capita média, real (ver DECISIONS.md).

Dois segmentos, nunca emendados: PNAD anual 2001–2015 (microdados) e PNAD Contínua 2012+ (SIDRA).
"""

from datetime import date

from .. import deflate
from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Flag, Indicador, Ponto, Quebra, Segmento, Subindicador
from ..sources import ibge_pnad_microdados as pnad
from ..sources import ibge_sidra
from ..validate import LIMIAR_CV_PADRAO, Auxiliares, Regras, ultimo_ano_transcorrido

TABELA = 7533
VAR_VALOR = 10816
VAR_CV = 10817
CLASSE_TOTAL = "1019[49243]"
CASAS = 0

# PNAD: mês de referência (setembro) e cobertura só urbana no Norte até 2003 (FONTES.md).
MES_REFERENCIA_PNAD = 9
UFS_COBERTURA_URBANA = ("11", "12", "13", "14", "15", "16")
FIM_COBERTURA_URBANA = 2003
# Conferência indireta: SIS 2016, Tabela 6.6, a preços de setembro de 2015 pelo INPC.
AUX_SIS = "sis2016_tab6_6"
ANO_PRECOS_SIS = 2015


class RendaPc:
    id = "renda_pc"
    regras = Regras(
        faixa=(0, 20_000),
        limiar_variacao=0.15,
        metodologias={"pnad": (2001, 2015), "pnadc": (2012, None)},
    )

    def __init__(self) -> None:
        self.auxiliares: Auxiliares = {}

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        pnadc = self._segmento_pnadc(hoje)
        ano_base = pnadc.anos[-1]
        segmentos = [self._segmento_pnad(ano_base), pnadc]
        return Indicador(
            id=self.id,
            nome="Renda domiciliar per capita média",
            tema="Renda",
            unidade="R$",
            unidade_detalhe=f"R$ de {ano_base} por mês (deflacionado pelo IPCA)",
            direcao="maior_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome="Renda domiciliar per capita")],
            segmentos=segmentos,
            quebras=[
                Quebra(
                    ano=2012,
                    texto=(
                        "Mudança de pesquisa: PNAD → PNAD Contínua. A amostra, o questionário e a "
                        "captação dos rendimentos mudaram; as séries não são diretamente "
                        "comparáveis. De 2012 a 2015 as duas pesquisas existem e os dois valores "
                        "são mostrados."
                    ),
                )
            ],
            escalas={"principal": escala_quantil(segmentos, CASAS)},
            versao_pipeline=versao_pipeline,
        )

    def _segmento_pnadc(self, hoje: date) -> Segmento:
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
                    ponto = Ponto(v=v, cv=cv, flags=_flags_cv(cv))
                valores.setdefault(geo, {})[str(ano)] = ponto

        return Segmento(
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
                "demais anos, da 1ª."
            ),
            anos=anos,
            valores=valores,
        )

    def _segmento_pnad(self, ano_base: int) -> Segmento:
        anos = pnad.ANOS
        ipca, ipca_em = deflate.indice_mensal(deflate.IPCA, anos[0], ano_base)
        inpc, _ = deflate.indice_mensal(deflate.INPC, anos[0], ANO_PRECOS_SIS)
        preco_base = deflate.media_anual(ipca, ano_base)
        inpc_sis = inpc[f"{ANO_PRECOS_SIS}{MES_REFERENCIA_PNAD:02d}"]

        valores: dict[str, dict[str, Ponto]] = {}
        for ano in anos:
            renda = pnad.renda_ano(ano)
            mes = f"{ano}{MES_REFERENCIA_PNAD:02d}"
            fator = preco_base / ipca[mes]
            for geo, est in renda.por_pessoa.items():
                cv = round(est.cv, 1) if est.cv is not None else None
                flags = _flags_cv(cv)
                if geo in UFS_COBERTURA_URBANA and ano <= FIM_COBERTURA_URBANA:
                    flags.append(Flag.COBERTURA_URBANA)
                valores.setdefault(geo, {})[str(ano)] = Ponto(
                    v=round(est.media * fator, 2), cv=cv, flags=flags
                )
            for geo, est in renda.por_domicilio_sis.items():
                chave = (AUX_SIS, "principal", "pnad", geo, ano)
                self.auxiliares[chave] = round(est.media * inpc_sis / inpc[mes], 2)

        manifest = carregar_manifest()
        baixado_em = max(manifest[a].baixado_em for ano in anos for a in pnad.ARQUIVOS[ano] if a)
        return Segmento(
            id="pnad",
            subindicador="principal",
            rotulo=f"PNAD ({anos[0]}–{anos[-1]})",
            fonte="IBGE – PNAD anual, microdados (cálculo do projeto)",
            fonte_url=pnad.URL_MICRODADOS,
            tabela=(
                "Microdados da PNAD; 2001–2012 com os pesos reponderados pela Projeção da "
                "População de 2013. Deflator: IPCA (SIDRA 1737, variável 2266)."
            ),
            extraido_em=max(baixado_em, ipca_em),
            notas=(
                "Calculado pelo projeto a partir dos microdados da PNAD, no mesmo conceito da "
                "PNAD Contínua: média por pessoa, incluindo quem mora em domicílio sem "
                "rendimento; sem pensionistas, empregados domésticos e seus parentes. "
                f"Valores de setembro de cada ano levados a preços médios de {ano_base} pelo "
                "IPCA. CV estimado pelo projeto com o plano amostral. "
                "Sem dados em 2010: ano de Censo, a PNAD não foi a campo. "
                f"Até {FIM_COBERTURA_URBANA} a PNAD não cobria a área rural de RO, AC, AM, RR, "
                "PA e AP (marcados como cobertura apenas urbana); o total do Brasil nesses anos "
                "também exclui essa área. O cálculo reproduz a Síntese de Indicadores Sociais "
                "2016 (Tabela 6.6) quando feito no conceito dela."
            ),
            anos=anos,
            valores=valores,
        )


def _flags_cv(cv: float | None) -> list[Flag]:
    return [Flag.BAIXA_PRECISAO] if cv is not None and cv > LIMIAR_CV_PADRAO else []
