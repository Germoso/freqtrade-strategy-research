#!/usr/bin/env bash
set -e
# Copiar config a directorio escribible y sustituir env vars
cp /freqtrade/user_data/config.json /tmp/config.json
python3 - <<'PY'
import os
p='/tmp/config.json'
with open(p) as f:
    raw=f.read()
for key in ['TELEGRAM_TOKEN','TELEGRAM_CHAT_ID']:
    val=os.environ.get(key,'')
    raw=raw.replace('${'+key+'}', val)
with open(p,'w') as f:
    f.write(raw)
PY
exec freqtrade trade --config /tmp/config.json --strategy SolEMACrossDetTrendFilterTP15SL20
PY
chmod +x /home/germoso/code/freqtrade-strategy-research/deploy/entrypoint.sh
echo done