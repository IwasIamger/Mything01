from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Herzlich Willkommen! Dein Flask-Bot läuft jetzt auf Render.com."

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    # Hier kannst du die Logik für den Webhook hinzufügen
    return jsonify({"message": "Webhook erhalten!", "data": data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)