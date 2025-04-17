from flask import Flask, request, jsonify
import MetaTrader5 as mt5

app = Flask(__name__)

# Initialisiere MetaTrader 5
if not mt5.initialize():
    print("MT5 konnte nicht initialisiert werden")
    quit()

@app.route('/', methods=['POST'])
def trade():
    data = request.get_json()

    action = data.get('action')
    symbol = data.get('symbol', 'XAUUSD')
    lots = data.get('lots', 0.1)

    if action not in ['buy', 'sell']:
        return jsonify({'status': 'error', 'message': 'Ungültige Aktion'}), 400

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None or not symbol_info.visible:
        return jsonify({'status': 'error', 'message': 'Symbol nicht verfügbar'}), 400

    price = mt5.symbol_info_tick(symbol).ask if action == 'buy' else mt5.symbol_info_tick(symbol).bid
    order_type = mt5.ORDER_TYPE_BUY if action == 'buy' else mt5.ORDER_TYPE_SELL

    request_trade = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lots,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python Bot Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request_trade)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return jsonify({'status': 'error', 'message': f'Order fehlgeschlagen: {result.retcode}'}), 500

    return jsonify({'status': 'ok', 'message': f'{action} Order gesendet'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)