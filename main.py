# main.py

from flask import Flask, request, jsonify
import MetaTrader5 as mt5

app = Flask(__name__)

# === MetaTrader5 initialisieren ===
if not mt5.initialize():
    print("MT5-Init fehlgeschlagen")
    quit()

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    symbol = data['symbol']
    lots   = float(data['lots'])
    action = data['action']  # "buy" oder "sell"

    # Tickpreise holen
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return jsonify({"error": f"Symbol {symbol} nicht verfügbar"}), 400

    price = tick.ask if action == "buy" else tick.bid
    order_type = mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL

    # Order-Request zusammenstellen
    request_data = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lots,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": f"Auto-{action} via TV",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    # Order absenden
    result = mt5.order_send(request_data)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return jsonify({
            "error": f"Trade fehlgeschlagen, Retcode={result.retcode}",
            "result": result._asdict()
        }), 500

    return jsonify({"status": "ok", "order": result._asdict()}), 200

if __name__ == "__main__":
    # Auf allen Interfaces auf Port 5000 lauschen
    app.run(host="0.0.0.0", port=5000)