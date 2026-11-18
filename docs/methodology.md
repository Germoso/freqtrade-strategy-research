# Metodología

## Backtesting

- Motor: Freqtrade (nativo, sin Docker), Python 3.12.
- Configuración base: `config/config-xau-okx-5m.json` (adaptar exchange/pares).
- Estrategia: `EMACrossDetTrendFilterTP15SL20`.
- Timeframe: 5m (probado también 1h).
- Modo: futures, dry-run (sin credenciales).
- Fee: 0.08% por lado (configurable).
- Slippage: no modelado explícitamente.

## Procedimiento

1. Descargar datos OHLCV para el par y timeframe.
2. Ejecutar backtest con `freqtrade backtesting`.
3. Extraer trades del JSON de resultados.
4. Calcular métricas base (winrate, profit, drawdown).
5. Aplicar filtro de rachas (EMA20 sobre secuencia +1/-1) en ambas direcciones.
6. Comparar resultados.

## Filtro de rachas

- Construir secuencia de resultados: +1 si win, -1 si loss.
- Calcular EMA20 sobre esa secuencia acumulada.
- **Filtro normal**: ejecutar trade solo si racha acumulada >= EMA.
- **Filtro invertido**: ejecutar trade solo si racha acumulada < EMA.
- Los trades no ejecutados se simulan (no afectan PnL, pero sí la curva de rachas).

## Validación

- In-sample: período completo disponible.
- Sub-períodos: últimos 3 meses, último mes.
- Out-of-sample: pendiente (no se ha reservado un período independiente para esta familia).

## Limitaciones

- Los datos de algunos pares son cortos (AKE desde julio 2026, ONDO desde mayo 2026).
- El filtro de rachas es un post-proceso, no una regla de entrada; no se ha validado en live.
- No se ha optimizado con hyperopt para esta estrategia específica.
- La muestra de trades filtrados puede ser pequeña (ej. 25 trades en XAU invertido).
PY
echo done