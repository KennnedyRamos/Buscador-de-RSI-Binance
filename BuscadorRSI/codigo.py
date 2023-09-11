'''Importar API com sua chave Key da Binance'''

from binance.client import Client
import ccxt
import time
# Importe sua pasta contendo sua Api_key 
from chaves import api_key, api_secret

apis = Client(api_key, api_secret)

# Configuração da API da Binance
apis = api_key, api_secret

exchange = ccxt.binance({

    'enableRateLimit': True,
})

# Função para buscar moedas em tempo real com base no RSI em vários intervalos de tempo
def busca_moedas_rsi():
    intervalos = [
        '5m',  # 5 minutos
        '15m',  # 15 minutos
        '1h',  # 1 hora
        '4h',  # 4 horas
        '12h',  # 12 horas
        '1d',  # 1 dia
        '1w',  # 1 semana
        '1M',  # 1 mês
    ]

    periodo_rsi = 14
    limiar_sobrevenda = 30
    limiar_sobrecompra = 70

    while True:
        for intervalo in intervalos:
            try:
                tickers = exchange.fetch_tickers()
                for symbol, ticker in tickers.items():
                    if 'USDT' in symbol:  # Verifica se o par é em relação ao USDT
                        candles = exchange.fetch_ohlcv(symbol, intervalo, limit=periodo_rsi + 1)  # Coleta dados do intervalo de tempo

                        if len(candles) >= periodo_rsi + 1:
                            closes = [candle[4] for candle in candles]
                            rs = sum([closes[i] - closes[i - 1] for i in range(1, periodo_rsi) if closes[i] > closes[i - 1]]) / sum(
                                [-closes[i] + closes[i - 1] for i in range(1, periodo_rsi) if closes[i] < closes[i - 1]])
                            rsi = 100 - (100 / (1 + rs))

                            if rsi >= limiar_sobrecompra:
                                print(f"{symbol} está sobrecomprado em {intervalo} (RSI: {rsi:.2f})")
                            elif rsi <= limiar_sobrevenda:
                                print(f"{symbol} está sobrevendido em {intervalo} (RSI: {rsi:.2f})")

            except Exception as e:
                print(f"Erro na busca em tempo real ({intervalo}): {e}")
                continue
            time.sleep(5)  # Intervalo entre as criptomoedas

        time.sleep(60)  # Aguardar 1 minuto antes de verificar novamente

if __name__ == "__main__":
    busca_moedas_rsi()
