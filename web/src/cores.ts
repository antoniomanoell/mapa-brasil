// Paleta sequencial de um só matiz (azuis do ColorBrewer), segura para daltônicos (PROJECT.md, 9.2).
// Pula o tom mais claro, que some no fundo. Mais escuro = maior valor, para qualquer indicador:
// a cor não diz o que é "bom" ou "ruim".

import { schemeBlues } from 'd3-scale-chromatic';

export const CLASSES = 5;
export const CORES: readonly string[] = (schemeBlues[CLASSES + 1] as readonly string[]).slice(1);
export const COR_BRASIL = '#6b6b6b';

/** Imagem 8×8 de hachura diagonal para "sem dado". */
export function hachura(): ImageData {
  const c = document.createElement('canvas');
  c.width = c.height = 8;
  const ctx = c.getContext('2d') as CanvasRenderingContext2D;
  ctx.fillStyle = '#e6e6e6';
  ctx.fillRect(0, 0, 8, 8);
  ctx.strokeStyle = '#a3a3a3';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(-2, 10);
  ctx.lineTo(10, -2);
  ctx.moveTo(-2, 2);
  ctx.lineTo(2, -2);
  ctx.moveTo(6, 10);
  ctx.lineTo(10, 6);
  ctx.stroke();
  return ctx.getImageData(0, 0, 8, 8);
}

export const CSS_HACHURA = 'repeating-linear-gradient(-45deg, #e6e6e6 0 3px, #a3a3a3 3px 4px)';
