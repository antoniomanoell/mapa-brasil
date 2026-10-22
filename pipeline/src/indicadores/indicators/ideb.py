"""`ideb` — Índice de Desenvolvimento da Educação Básica, três etapas (ver DECISIONS.md).

Anos iniciais e finais: rede pública. Ensino médio: rede estadual, porque o INEP não publica a rede
pública do ensino médio por UF (e é a rede estadual que o próprio INEP divulga como "rede pública"
do estado). O Ideb é bienal: anos ímpares de 2005 em diante; os pares não existem.
"""

from datetime import date

from ..escala import escala_quantil
from ..raw_manual import carregar_manifest
from ..schema import Indicador, Ponto, Segmento, Subindicador
from ..sources import inep_ideb
from ..validate import Regras, ultimo_ano_transcorrido

CASAS = 1
# etapa → (nome, rede usada)
ETAPAS = {
    "anos_iniciais": ("Anos iniciais do ensino fundamental (rede pública)", "Pública"),
    "anos_finais": ("Anos finais do ensino fundamental (rede pública)", "Pública"),
    "medio": ("Ensino médio (rede estadual)", "Estadual"),
}
NOTA_2021 = (
    "Para 2021, ano de pandemia, o INEP remete à nota informativa do Ideb 2021 sobre as condições "
    "do cálculo."
)


class Ideb:
    id = "ideb"
    regras = Regras(faixa=(0, 10), limiar_variacao=0.15, metodologias={"inep": (2005, None)})

    def construir(self, versao_pipeline: str, hoje: date) -> Indicador:
        ate = ultimo_ano_transcorrido(hoje)
        segmentos = []
        for etapa_id, (_nome, rede) in ETAPAS.items():
            serie = inep_ideb.etapa(etapa_id, rede)
            anos = sorted({a for por_ano in serie.values() for a in por_ano if a <= ate})
            valores = {
                geo: {
                    str(a): (
                        Ponto(v=por_ano[a])
                        if por_ano.get(a) is not None
                        else Ponto(v=None, lacuna="Ideb não calculado pelo INEP")
                    )
                    for a in anos
                }
                for geo, por_ano in sorted(serie.items())
            }
            nota_rede = (
                "Rede estadual: o INEP não publica a rede pública do ensino médio por UF. "
                if rede == "Estadual"
                else "Rede pública (estadual, municipal e federal). "
            )
            segmentos.append(
                Segmento(
                    id="inep",
                    subindicador=etapa_id,
                    rotulo=f"INEP ({anos[0]}–{anos[-1]}, bienal)",
                    fonte="INEP – Ideb (Saeb e Censo Escolar)",
                    fonte_url=inep_ideb.URL,
                    tabela=(
                        "divulgacao_regioes_ufs_ideb_2025 e divulgacao_brasil_ideb_2025, "
                        f"rede {rede}"
                    ),
                    extraido_em=carregar_manifest()[inep_ideb.ARQUIVO_UFS].baixado_em,
                    notas=(
                        f"{nota_rede}O Ideb é calculado a cada dois anos (anos ímpares): não há "
                        f"valor nos anos pares. {NOTA_2021}"
                    ),
                    anos=anos,
                    valores=valores,
                )
            )
        return Indicador(
            id=self.id,
            nome="Ideb",
            tema="Educação",
            unidade="índice",
            unidade_detalhe="índice de 0 a 10",
            direcao="maior_melhor",
            casas_decimais=CASAS,
            tipo_valor="medido",
            subindicadores=[Subindicador(id=e, nome=n) for e, (n, _) in ETAPAS.items()],
            segmentos=segmentos,
            escalas={s.subindicador: escala_quantil([s], CASAS) for s in segmentos},
            versao_pipeline=versao_pipeline,
        )
