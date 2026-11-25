FROM freqtradeorg/freqtrade:stable

# Copiar estrategia
COPY strategies/EMAAlignmentAlerts.py /freqtrade/user_data/strategies/EMAAlignmentAlerts.py

# Copiar config
COPY deploy/config.json /freqtrade/user_data/config.json

# Copiar entrypoint
COPY deploy/entrypoint.sh /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["sh", "/entrypoint.sh"]
