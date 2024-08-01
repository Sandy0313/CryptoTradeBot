from flask import Flask, Blueprint, request, jsonify
from werkzeug.exceptions import HTTPException
from your_trade_controller import (
    create_trade, update_trade, delete_trade, get_trade, get_all_trades
)

trade_ops = Blueprint('trade_ops', __name__)

@trade_ops.route('/trades', methods=['POST'])
def create_trade_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        result = create_trade(data)
        if not result:
            return jsonify({"error": "Trade could not be created"}), 500
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trade_ops.route('/trades/<int:trade_id>', methods=['PUT'])
def update_trade_route(trade_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        result = update_trade(trade_id, data)
        if result is None: 
            return jsonify({"error": "Trade not found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trade_ops.route('/trades/<int:trade_id>', methods=['DELETE'])
def delete_trade_route(trade_id):
    try:
        result = delete_trade(trade_id)
        if result is None:
            return jsonify({"error": "Trade not found"}), 404
        return jsonify(result), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trade_ops.route('/trades/<int:trade_id>', methods=['GET'])
def get_trade_route(trade_id):
    try:
        result = get_trade(trade_id)
        if result is None:
            return jsonify({"error": "Trade not found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@trade_ops.route('/trades', methods=['GET'])
def get_all_trades_route():
    try:
        result = get_all_trades()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Handle HTTP exceptions globally"""
    response = e.get_response()
    response.data = jsonify({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

app = Flask(__name__)
app.register_blueprint(trade_ops, url_prefix='/api')

if __name__ == '__main__':
    from os import environ
    app.run(
        host=environ.get('HOST', '127.0.0.1'), 
        port=environ.get('PORT', 5000)
    )