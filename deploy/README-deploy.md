# Monitor de alineación de EMAs en Dokploy

Configura la aplicación para construir desde la raíz del repositorio con
`deploy/Dockerfile`. La imagen arranca `EMAAlignmentAlerts` en modo de
simulación con cero operaciones habilitadas.

Por defecto monitorea SOL/USDT perpetuo de Binance en velas de 5 minutos.
Ajusta `exchange.pair_whitelist` y `timeframe` en `deploy/config.json` si
quieres cambiar el mercado o la temporalidad.

- Alcista — EMA 10 > EMA 20 > EMA 50 > EMA 200.
- Bajista — EMA 10 < EMA 20 < EMA 50 < EMA 200.

El aviso sale al cierre de la primera vela alineada en cada dirección.
Los avisos se registran en los logs de la aplicación.

## Telegram

Configura `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID` en las variables de entorno
de la aplicación para recibir los avisos. La configuración habilita los
mensajes personalizados de Freqtrade.

Si expones el dashboard, configura también `API_USER`, `API_PASSWORD`,
`JWT_SECRET` y `WS_TOKEN` en la aplicación.

## Redespliegue

Con el despliegue automático activo, un push a la rama conectada reconstruye
la aplicación con la nueva estrategia. También puedes usar **Build & Deploy**
en Dokploy. En los logs de inicio deben aparecer `EMAAlignmentAlerts` y
`RUNNING`.
