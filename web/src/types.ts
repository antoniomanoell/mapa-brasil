// Espelho do formato publicado pelo pipeline (pipeline/src/indicadores/schema.py).
// O JSON é gravado com exclude_defaults: campos com valor padrão podem faltar.

export type Flag = 'baixa_precisao' | 'cobertura_urbana' | 'estimativa' | 'preliminar';

export interface Ponto {
  v: number | null;
  n?: number | null;
  cv?: number | null;
  ic?: [number, number] | null;
  flags?: Flag[];
  lacuna?: string | null;
}

export interface Segmento {
  id: string;
  subindicador: string;
  papel?: 'principal' | 'referencia';
  rotulo: string;
  fonte: string;
  fonte_url: string;
  tabela: string;
  extraido_em: string;
  notas?: string;
  // Área de onde vem o valor de cada UF, quando não é a UF inteira (ex.: IPCA da região
  // metropolitana).
  areas?: Record<string, string>;
  anos: number[];
  valores: Record<string, Record<string, Ponto>>;
}

export interface Subindicador {
  id: string;
  nome: string;
}

export interface Quebra {
  ano: number;
  texto: string;
}

export interface Escala {
  tipo: 'quantil';
  limites: number[];
}

export interface Indicador {
  id: string;
  nome: string;
  tema: string;
  unidade: string;
  unidade_detalhe: string;
  direcao: 'maior_melhor' | 'menor_melhor';
  casas_decimais: number;
  tipo_valor: 'medido' | 'estimativa';
  subindicadores: Subindicador[];
  segmentos: Segmento[];
  quebras?: Quebra[];
  escalas: Record<string, Escala>;
  versao_pipeline: string;
}

export interface ItemCatalogo {
  id: string;
  nome: string;
  tema: string;
  unidade: string;
  subindicadores: Subindicador[];
  ano_inicial: number;
  ano_final: number;
  arquivo: string;
}

export interface Catalogo {
  gerado_em: string;
  versao_pipeline: string;
  indicadores: ItemCatalogo[];
}
