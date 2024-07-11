import os
from flask import Flask, request, jsonify
import ccxt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Lista de corretoras
exchanges = ['binance', 'kraken', 'coinbase', 'ascendex','woo', 'phemex','xt','whitebit', 'bigone', 'bingx']


# Função para obter a taxa de câmbio do dólar
def get_usd_exchange_rate():
    # Aqui você implementaria a lógica para obter a taxa de câmbio do dólar
    # de uma fonte de dados confiável
    # Por exemplo, usando uma API como a Alpha Vantage
    # Substitua isso pelo código real de obtenção da taxa de câmbio
    return 5.20  # Este é um valor de exemplo

# Obter livros de ordens
def get_order_books(symbols):
    order_books = {}
    for symbol in symbols:
        order_books[symbol] = {}
        for exchange_id in exchanges:
            try:
                exchange = getattr(ccxt, exchange_id)()
                order_book = exchange.fetch_order_book(symbol, limit=10)
                order_books[symbol][exchange_id] = order_book
            except Exception as e:
                print(f"Erro ao obter livro de ordens da {exchange_id} para {symbol}: {e}")
    return order_books

# Lógica de arbitragem
def arbitrage_logic(symbols, usd_exchange_rate):
    arbitrage_data = {}
    for symbol in symbols:
        arbitrage_data[symbol] = {}
        order_books = get_order_books([symbol])
        for exchange_id, order_book in order_books[symbol].items():
            bids = order_book['bids'][:10]
            asks = order_book['asks'][:10]
            spread = asks[0][0] - bids[0][0]
            # Aqui você pode implementar a lógica para calcular taxas, se disponíveis
            # Substitua isso pelo seu código real de cálculo de taxas
            arbitrage_data[symbol][exchange_id] = {
                'bids': bids,
                'asks': asks,
                'spread': spread
            }
    return arbitrage_data

@app.route('/arbitrage', methods=['GET'])
def arbitrage():
    # Obter parâmetros da solicitação
    usd_exchange_rate = float(request.args.get('usd_exchange_rate'))
    symbols =  ['BTC/USDT', 'ETH/USDT', 'LTC/USDT']

    # Obter dados de arbitragem
    arbitrage_data = arbitrage_logic(symbols, usd_exchange_rate)

    # Estruturar dados em JSON
    json_data = {
        'usd_exchange_rate': usd_exchange_rate,
        'arbitrage_data': arbitrage_data
    }

    return jsonify(json_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)