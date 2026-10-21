import type { Catalogo, Indicador, Ponto, Segmento } from '../src/types';
import { BR, UFS } from '../src/ufs';

function seg(id: string, sub: string, anos: number[], base = 10): Segmento {
  const valores: Record<string, Record<string, Ponto>> = {};
  [...UFS.map((u) => u.codigo), BR].forEach((geo, i) => {
    valores[geo] = Object.fromEntries(anos.map((a) => [String(a), { v: base + i + a / 1000 }]));
  });
  return {
    id,
    subindicador: sub,
    rotulo: id.toUpperCase(),
    fonte: 'Teste',
    fonte_url: 'https://exemplo.gov.br',
    tabela: '0',
    extraido_em: '2026-10-20',
    anos,
    valores,
  };
}

/** Indicador com sobreposição PNAD (2001–2015, sem 2010) e PNADC (2012–2025), e dois subindicadores. */
export const IND: Indicador = {
  id: 'teste',
  nome: 'Teste',
  tema: 'Renda',
  unidade: 'R$',
  unidade_detalhe: 'R$ de 2025',
  direcao: 'maior_melhor',
  casas_decimais: 0,
  tipo_valor: 'medido',
  subindicadores: [
    { id: 'geral', nome: 'Geral' },
    { id: 'outro', nome: 'Outro' },
  ],
  segmentos: [
    seg(
      'pnad',
      'geral',
      [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2011, 2012, 2013, 2014, 2015],
    ),
    seg(
      'pnadc',
      'geral',
      [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    ),
    seg('censo', 'outro', [2000, 2010]),
  ],
  escalas: {
    geral: { tipo: 'quantil', limites: [12, 18, 24, 30] },
    outro: { tipo: 'quantil', limites: [1, 2, 3, 4] },
  },
  versao_pipeline: 'abc',
};

export const CAT: Catalogo = {
  gerado_em: '2026-10-20',
  versao_pipeline: 'abc',
  indicadores: [
    {
      id: 'teste',
      nome: 'Teste',
      tema: 'Renda',
      unidade: 'R$',
      subindicadores: IND.subindicadores,
      ano_inicial: 2001,
      ano_final: 2025,
      arquivo: 'indicators/teste.json',
    },
    {
      id: 'outro',
      nome: 'Outro',
      tema: 'Segurança',
      unidade: '%',
      subindicadores: [{ id: 'principal', nome: 'Outro' }],
      ano_inicial: 2000,
      ano_final: 2024,
      arquivo: 'indicators/outro.json',
    },
  ],
};
