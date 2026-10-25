from flask import Flask, jsonify
from bcv import bcv

app = Flask(__name__)


@app.route("/", methods=["GET"])
@app.route("/api/dolar", methods=["GET"])
def get_dolar():
    try:
        amount = bcv.get_amount_bcv()
        return jsonify({
            "success": True,
            "moneda": "USD",
            "dolar": amount,
            "valor_float": float(amount.replace(",", "."))
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
