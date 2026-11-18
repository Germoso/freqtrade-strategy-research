#!/usr/bin/env bash
set -e
cp /freqtrade/user_data/config.json /tmp/config.json
python3 - <<'PYEOF'
import os
p='/tmp/config.json'
with open(p) as f:
    raw=f.read()
defaults = {
    'TELEGRAM_TOKEN': '',
    'TELEGRAM_CHAT_ID': '',
    'API_USER': 'freqtrade',
    'API_PASSWORD': 'freqtrade',
    'JWT_SECRET': 'change-me-jwt-secret',
    'WS_TOKEN': 'change-me-ws-token',
}
for key, default in defaults.items():
    val = os.environ.get(key, default)
    if not val:
        val = default
    raw = raw.replace('${' + key + '}', val)
with open(p,'w') as f:
    f.write(raw)
PYEOF
exec freqtrade trade --config /tmp/config.json --strategy EMACrossDetTrendFilterTP15SL20
