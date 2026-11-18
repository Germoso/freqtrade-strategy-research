FROM freqtradeorg/freqtrade:stable

# Copiar estrategia
COPY strategies/ /freqtrade/user_data/strategies/

# Copiar config (sin secretos; usar env vars en runtime)
COPY deploy/config.json /freqtrade/user_data/config.json

# Puerto de la API (opcional)
EXPOSE 8080

CMD ["freqtrade", "trade", "--config", "user_data/config.json", "--strategy", "SolEMACrossDetTrendFilterTP15SL20"]
