# Deploy en Dokploy (Freqtrade + alertas)

## Objetivo
Desplegar Freqtrade en modo dry-run para que genere señales y envíe alertas (Telegram),
sin ejecutar trades reales. Tú decides manualmente si entras.

## Pasos

1. **Subir el repo a Dokploy**
   - Crear una nueva Application en Dokploy.
   - Conectar el repo de GitHub.
   - Seleccionar el Dockerfile en `deploy/Dockerfile`.

2. **Variables de entorno en Dokploy**
   - `TELEGRAM_TOKEN`: token del bot de Telegram.
   - `TELEGRAM_CHAT_ID`: tu chat ID.
   - (Opcional) `EXCHANGE_API_KEY`, `EXCHANGE_SECRET` si quieres datos privados (no necesario para dry-run).
   - (Opcional) `PORT`: puerto host a exponer (default 8080).
   - (Opcional) `API_USER`, `API_PASSWORD`, `JWT_SECRET`, `WS_TOKEN`: credenciales del dashboard/API web (defaults inseguros; cámbialos en producción).

3. **Config**
   - El `deploy/config.json` ya tiene `dry_run: true` y Telegram habilitado.
   - Ajusta `pair_whitelist` al par que quieras monitorear (SOL, LINK, XAU, etc.).
   - El token de Telegram se inyecta vía `${TELEGRAM_TOKEN}` (Dokploy lo resuelve).

4. **Deploy**
   - Build & Deploy en Dokploy.
   - Verifica logs: deberías ver "freqtrade" arrancando y "Telegram notification sent".

5. **Alertas**
   - Cuando la estrategia detecte una entrada/salida, te llegará un mensaje a Telegram.
   - Tú decides si pones el trade manualmente en tu exchange.

## Notas
- **No commitear secretos**: las API keys van solo en Dokploy (env vars).
- **Datos**: el contenedor descarga datos al arrancar; asegura que el exchange esté accesible.
- **Uptime**: Dokploy reinicia el contenedor si cae.
- **Dry-run**: `dry_run: true` evita ejecución real. Para live trading, cambia a `false` y añade API keys (no recomendado sin validación).

## Alternativa nativa (sin Docker)
Si prefieres nativo (según tu preferencia), usa un VPS con systemd:
```bash
freqtrade trade --config user_data/config.json --strategy EMACrossDetTrendFilterTP15SL20
```
Y configura un servicio systemd para que arranque al boot.
PY
echo done