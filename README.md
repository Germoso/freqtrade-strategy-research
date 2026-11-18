# Freqtrade Strategy Research — EMA Cross + Trend Filter

Repositorio de investigación de estrategias para Freqtrade (futures, 5m/1h), con la estrategia principal
`SolEMACrossDetTrendFilterTP15SL20` y un filtro de capital basado en rachas (win/loss).

## Estrategia principal

`SolEMACrossDetTrendFilterTP15SL20` (ver `strategies/SolEMACrossDetTrendFilterTP15SL20.py`):

- **Entradas**: cruce EMA10/EMA20, solo si van a favor de la EMA200.
  - Long: EMA10 cruza arriba de EMA20 **y** precio > EMA200.
  - Short: EMA10 cruza abajo de EMA20 **y** precio < EMA200.
- **Salidas**: TP fijo 1.5%, SL fijo 2.0% (R:R 0.75).
- **Timeframe**: 5m (probado también en 1h).
- **Modo**: research/backtest (no operar con dinero real sin validación).

## Filtro de capital (rachas)

Sobre la secuencia de resultados (+1 win, -1 loss) se calcula una EMA20. Un trade se "ejecuta"
(afecta el PnL) solo si la racha acumulada está por encima (filtro normal) o por debajo
(filtro invertido) de la EMA. Los trades simulados no afectan el PnL.

- **Filtro normal** (entrar en racha ganadora): funciona mejor en LINK (persistencia de rachas).
- **Filtro invertido** (entrar en racha perdedora): funciona mejor en SOL (mean reversion en rachas).

## Resultados resumidos

### SOL/USDT (2025-01 → 2026-10, 5m)
| Escenario | Trades | Winrate | Profit | Drawdown |
|---|---|---|---|---|
| Base (sin filtro) | 1454 | 58.39% | -25.12% | 26.63% |
| Filtro invertido | 313 | 62.30% | **+1.01%** | 5.50% |

### LINK/USDT (2026-01-19 → 2026-10-17, 5m)
| Escenario | Trades | Winrate | Profit | Drawdown |
|---|---|---|---|---|
| Base | 299 | 59.87% | -3.32% | 11.02% |
| Filtro normal | 225 | 63.11% | **+1.91%** | 5.48% |

### XAU/USDT (OKX, 2025-04-09 → 2026-11-12, 5m)
| Escenario | Trades | Winrate | Profit | Drawdown |
|---|---|---|---|---|
| Base | 239 | 63.18% | +2.74% | 1.51% |
| Filtro normal | 214 | 62.62% | +2.03% | — |
| Filtro invertido | 25 | 68.00% | +0.71% | — |

### 10 pares (últimos 3 meses)
Ver `docs/results.md` para la tabla completa. Resumen de profit total acumulado:
- Base: -6748.54 USDT
- Normal: -4242.07 USDT
- Invertido: -2506.47 USDT

## Requisitos

- Python 3.12
- Freqtrade instalado (nativo, sin Docker): `freqtrade-src/.venv/`
- Datos OHLCV en `user_data/data/<exchange>/futures/`

## Replicación

1. Instalar Freqtrade nativamente (ver documentación oficial).
2. Copiar `strategies/SolEMACrossDetTrendFilterTP15SL20.py` a `user_data/strategies/`.
3. Usar un config como `config/config-xau-okx-5m.json` (ajustar exchange/pares).
4. Descargar datos:
   ```
   freqtrade download-data --exchange okx --pairs XAU/USDT:USDT --timeframe 5m --trading-mode futures
   ```
5. Ejecutar backtest:
   ```
   freqtrade backtesting --config config-xau-okx-5m.json \
     --strategy SolEMACrossDetTrendFilterTP15SL20 \
     --pairs "XAU/USDT:USDT" --timeframe 5m \
     --datadir user_data/data/okx --timerange 20250409-
   ```
6. Aplicar el filtro de rachas con los scripts en `tools/` (pendiente de publicar).

## Estructura

```
strategies/   # estrategia principal
config/       # configs de ejemplo
docs/         # metodología y resultados detallados
results/      # CSVs de trades y resúmenes
tools/        # scripts auxiliares
```

## Notas

- Los resultados son exploratorios. No operar con dinero real sin validación out-of-sample.
- El filtro de rachas es un post-proceso sobre la secuencia de trades, no una regla de entrada.
- La dirección del filtro (normal vs invertido) depende del activo.
PY
echo done