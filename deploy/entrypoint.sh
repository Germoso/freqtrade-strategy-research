#!/usr/bin/env bash
set -e
cp /freqtrade/user_data/config.json /tmp/config.json
python3 - <<'PYEOF'
import os
p='/tmp/config.json'
with open(p) as f:
    raw=f.read()
for key in ['TELEGRAM_TOKEN','TELEGRAM_CHAT_ID']:
    val=os.environ.get(key,'')
    raw=raw.replace('${'+key+'}', val)
with open(p,'w') as f:
    f.write(raw)
PYEOF
exec freqtrade trade --config /tmp/config.json --strategy EMACrossDetTrendFilterTP15SL20
EOF
cat -n /home/germoso/code/freqtrade-strategy-research/deploy/entrypoint.sh