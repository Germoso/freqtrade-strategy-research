#!/bin/sh
set -e

umask 077
python3 - <<'PY'
import json
import os

with open("/freqtrade/user_data/config.json") as source:
    config = json.load(source)

token = os.environ.get("TELEGRAM_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")
if token and chat_id:
    config["telegram"].update(token=token, chat_id=chat_id)
else:
    config.pop("telegram", None)
    print("Telegram sin configurar. Las alertas se registrarán en los logs.", flush=True)

for field, variable, default in (
    ("username", "API_USER", "freqtrade"),
    ("password", "API_PASSWORD", "freqtrade"),
    ("jwt_secret_key", "JWT_SECRET", "this-is-a-very-long-jwt-secret-key-123456"),
    ("ws_token", "WS_TOKEN", "change-me-ws-token"),
):
    config["api_server"][field] = os.environ.get(variable) or default

with open("/tmp/config.json", "w") as destination:
    json.dump(config, destination)
PY

exec freqtrade trade --config /tmp/config.json --strategy EMAAlignmentAlerts --db-url sqlite:///:memory:
