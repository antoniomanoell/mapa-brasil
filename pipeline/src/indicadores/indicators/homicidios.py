"""`homicidios` — taxa de homicídios por 100 mil habitantes (ver DECISIONS.md)."""

from datetime import date

from ..escala import escala_quantil
from ..population import FONTE as FONTE_POP
from ..population import populacao
from ..schema import Indicador, Ponto, Segmento, Subindicador
from ..sources import datasus_sim
from ..validate import Regras, ultimo_ano_transcorrido

ANO_INICIAL = 2000
CASAS = 1


class Homicidios:
    id = "homicidios"
    regras = Regras(
        faixa=(0, 200),
        # Taxas de UFs pequenas oscilam muito de um ano para outro.
        limiar_variacao=0.35,
        # CID-10 no SIM desde 1996.
        metodologias={"sim": (1996, None)},
    )

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        preliminares = datasus_sim.anos_preliminares()
        ultimo = min(ultimo_ano_transcorrido(hoje), min(preliminares) - 1)
        anos = list(range(ANO_INICIAL, ultimo + 1))
        pop = populacao(ultimo)
        grupos = [datasus_sim.GRUPO_AGRESSOES, datasus_sim.GRUPO_INTERVENCOES_LEGAIS]

        valores: dict[str, dict[str, Ponto]] = {}
        extracoes: list[date] = []
        for ano in anos:
            obitos, obtido_em = datasus_sim.obitos_por_uf(ano, grupos)
            extracoes.append(obtido_em)
            for geo, n in obitos.items():
                taxa = n / pop[geo][ano] * 100_000
                valores.setdefault(geo, {})[str(ano)] = Ponto(v=round(taxa, 2), n=n)

        anos_prelim = ", ".join(str(a) for a in sorted(preliminares))
        seg = Segmento(
            id="sim",
            subindicador="principal",
            rotulo=f"SIM/DATASUS ({anos[0]}–{anos[-1]})",
            fonte=f"Ministério da Saúde – SIM (DATASUS); população: {FONTE_POP}",
            fonte_url=datasus_sim.URL_FORMULARIO,
            tabela=(
                "TabNet obt10uf.def — óbitos p/ residência, grupos CID-10 Agressões (X85–Y09) "
                "e Intervenções legais e operações de guerra (Y35–Y36)"
            ),
            extraido_em=min(extracoes),
            notas=(
                f"Só anos com o SIM consolidado: o DATASUS declara {anos_prelim} como "
                "preliminares. O total Brasil inclui óbitos com UF de residência ignorada ou no "
                "exterior. A taxa usa a população das Projeções do IBGE (Revisão 2024), a mesma "
                "série de todo o site; por isso pode diferir levemente da publicada pelo Atlas da "
                "Violência, que usa outra população."
            ),
            anos=anos,
            valores=dict(sorted(valores.items())),
        )
        return Indicador(
            id=self.id,
            nome="Taxa de homicídios",
            tema="Segurança",
            unidade="por 100 mil hab.",
            unidade_detalhe="óbitos por agressão e intervenção legal por 100 mil habitantes",
            direcao="menor_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id="principal", nome="Taxa de homicídios")],
            segmentos=[seg],
            escalas={"principal": escala_quantil([seg], CASAS)},
            versao_pipeline=versao_pipeline,
        )
