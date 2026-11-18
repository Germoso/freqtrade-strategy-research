FROM freqtradeorg/freqtrade:stable

# Copiar estrategia
COPY strategies/ /freqtrade/user_data/strategies/

# Copiar config (con placeholders ${TELEGRAM_TOKEN})
COPY deploy/config.json /freqtrade/user_data/config.json

# Copiar entrypoint
COPY deploy/entrypoint.sh /entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["sh", "/entrypoint.sh"]
