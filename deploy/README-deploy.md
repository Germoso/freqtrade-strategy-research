# Monitor de alineación de EMAs en Dokploy

Configura la aplicación para construir desde la raíz del repositorio con
`deploy/Dockerfile`. La imagen arranca `EMAAlignmentAlerts` en modo de
simulación con cero operaciones habilitadas.

Monitorea en velas de 5 minutos los 50 perpetuos USDT de Bybit con mayor
volumen negociado en USDT durante las últimas 24 horas. Freqtrade actualiza
la lista cada 30 minutos mediante `VolumePairList`.

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

## Dominio en Dokploy

Para un despliegue con `deploy/docker-compose.yml`, abre **Domains** y
asigna tu host al servicio `freqtrade`, con **Path** `/` y **Container Port**
`8080`. El proxy llega al contenedor por la red de Dokploy. Para un dominio
propio, verifica que el registro DNS apunte al servidor. Guarda y vuelve a
desplegar el Compose para aplicar la ruta.

## Redespliegue

Con el despliegue automático activo, un push a la rama conectada reconstruye
la aplicación con la nueva estrategia. También puedes usar **Build & Deploy**
en Dokploy. En los logs de inicio deben aparecer `EMAAlignmentAlerts` y
`RUNNING`.
