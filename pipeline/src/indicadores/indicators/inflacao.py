"""`inflacao` — variação dos preços acumulada no ano (dezembro sobre dezembro), IPCA e INPC.

O IBGE não calcula esses índices por UF: publica-os para 16 áreas (regiões metropolitanas e
capitais). Cada UF que tem uma área mostra o valor dela, sempre com o nome da área; as demais ficam
sem dado (DECISIONS.md). Cada índice é uma série só: as tabelas do SIDRA mudam quando o IBGE
atualiza a estrutura de pesos, mas o índice é o mesmo e a série histórica nacional (tabelas 1737 e
1736) é contínua.
"""

from datetime import date

from ..escala import escala_quantil
from ..schema import Indicador, Ponto, Segmento, Subindicador
from ..sources import ibge_sidra
from ..ufs import BR, CODIGOS_UF
from ..validate import Regras, ultimo_ano_transcorrido

CASAS = 2
INICIO = 2000
CLASSIFICACAO = "315[7169]"  # índice geral

# Por índice: variável "acumulada no ano" e tabelas do SIDRA por período (último ano None = atual).
TABELAS: dict[str, tuple[int, list[tuple[int, int, int | None]]]] = {
    "ipca": (69, [(657, 2000, 2005), (2938, 2006, 2011), (1419, 2012, 2019), (7060, 2020, None)]),
    "inpc": (68, [(651, 2000, 2005), (2951, 2006, 2011), (1100, 2012, 2019), (7063, 2020, None)]),
}
NOMES = {"ipca": "IPCA", "inpc": "INPC"}

# Área do índice em cada UF (código do SIDRA → nome). Os dois primeiros dígitos são os da UF.
AREAS = {
    "1501": "RM de Belém",
    "2301": "RM de Fortaleza",
    "2601": "RM do Recife",
    "2901": "RM de Salvador",
    "3101": "RM de Belo Horizonte",
    "3201": "RM da Grande Vitória",
    "3301": "RM do Rio de Janeiro",
    "3501": "RM de São Paulo",
    "4101": "RM de Curitiba",
    "4301": "RM de Porto Alegre",
    "1200401": "Rio Branco",
    "2111300": "São Luís",
    "2800308": "Aracaju",
    "5002704": "Campo Grande",
    "5208707": "Goiânia",
    "5300108": "Brasília",
}
# Áreas que entraram no índice no meio do ano: o acumulado desse ano não cobre o ano todo.
ENTRADA_NO_MEIO_DO_ANO = {"1200401": 2018, "2111300": 2018, "2800308": 2018}

SEM_AREA = "o IBGE não calcula o índice para nenhuma área deste estado"
ANTES_DA_ENTRADA = "a área deste estado ainda não fazia parte do índice"
ANO_INCOMPLETO = "a área entrou no índice em maio de 2018: o acumulado do ano cobre só 8 meses"


class Inflacao:
    id = "inflacao"
    regras = Regras(
        faixa=(-5, 40),
        limiar_variacao=1.0,
        metodologias={"ipca": (INICIO, None), "inpc": (INICIO, None)},
    )

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        segmentos = [self._segmento(sub, hoje) for sub in TABELAS]
        return Indicador(
            id=self.id,
            nome="Inflação (IPCA e INPC)",
            tema="Preços",
            unidade="%",
            unidade_detalhe=(
                "% de variação dos preços no ano (dezembro sobre dezembro), na região "
                "metropolitana ou capital do estado"
            ),
            direcao="menor_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[
                Subindicador(
                    id="ipca", nome="IPCA (famílias com renda de 1 a 40 salários mínimos)"
                ),
                Subindicador(id="inpc", nome="INPC (famílias com renda de 1 a 5 salários mínimos)"),
            ],
            segmentos=segmentos,
            escalas={s.subindicador: escala_quantil([s], CASAS) for s in segmentos},
            versao_pipeline=versao_pipeline,
        )

    def _segmento(self, sub: str, hoje: date) -> Segmento:
        variavel, tabelas = TABELAS[sub]
        fim = ultimo_ano_transcorrido(hoje)
        por_area: dict[str, dict[int, float]] = {}
        usadas: list[str] = []
        extraido: list[date] = []
        for tabela, ini, fim_tabela in tabelas:
            ate = min(fim_tabela or fim, fim)
            if ate < ini:
                continue
            meses = [f"{a}12" for a in range(ini, ate + 1)]
            dados, obtido_em = ibge_sidra.consultar_areas_mensal(
                tabela, variavel, meses, CLASSIFICACAO
            )
            usadas.append(f"{tabela} ({ini}–{ate})")
            extraido.append(obtido_em)
            for area, serie in dados.items():
                for mes, v in serie.items():
                    if v is not None:
                        por_area.setdefault(area, {})[int(mes[:4])] = v
        novas = set(por_area) - set(AREAS) - {BR}
        if novas:
            raise ValueError(f"{NOMES[sub]}: áreas novas no SIDRA, sem UF definida: {novas}")

        anos = list(range(INICIO, fim + 1))
        area_da_uf = {codigo[:2]: codigo for codigo in AREAS}
        valores: dict[str, dict[str, Ponto]] = {}
        for geo in [BR, *sorted(CODIGOS_UF)]:
            area = BR if geo == BR else area_da_uf.get(geo)
            serie = por_area.get(area, {}) if area else {}
            for ano in anos:
                v = serie.get(ano)
                if area is None:
                    ponto = Ponto(v=None, lacuna=SEM_AREA)
                elif ENTRADA_NO_MEIO_DO_ANO.get(area) == ano:
                    ponto = Ponto(v=None, lacuna=ANO_INCOMPLETO)
                elif v is None:
                    ponto = Ponto(v=None, lacuna=ANTES_DA_ENTRADA)
                else:
                    ponto = Ponto(v=v)
                valores.setdefault(geo, {})[str(ano)] = ponto

        return Segmento(
            id=sub,
            subindicador=sub,
            rotulo=f"{NOMES[sub]} ({INICIO}–)",
            fonte=f"IBGE – Sistema Nacional de Índices de Preços ao Consumidor ({NOMES[sub]})",
            fonte_url=ibge_sidra.url_tabela(tabelas[-1][0]),
            tabela=(
                f"SIDRA {', '.join(usadas)}, variável {variavel} (variação acumulada no ano), "
                "dezembro de cada ano, índice geral"
            ),
            extraido_em=max(extraido),
            notas=(
                "O IBGE não calcula o índice por estado: cada estado mostra a sua região "
                "metropolitana ou capital. Até 2013 eram 11 áreas; Grande Vitória e Campo Grande "
                "entraram em janeiro de 2014, e Rio Branco, São Luís e Aracaju em maio de 2018 (o "
                "acumulado de 2018 dessas três não cobre o ano todo e fica sem dado). Rondônia, "
                "Amazonas, Roraima, Amapá, Tocantins, Piauí, Rio Grande do Norte, Paraíba, "
                "Alagoas, Mato Grosso e Santa Catarina não têm área no índice."
            ),
            areas={codigo[:2]: nome for codigo, nome in AREAS.items()},
            anos=anos,
            valores=valores,
        )
