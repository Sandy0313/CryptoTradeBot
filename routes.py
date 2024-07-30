from flask import Flask, Blueprint, request, jsonify
from your_trade_controller import create_trade, update_trade, delete_trade, get_trade, get_all_trades

trade_ops = Blueprint('trade_ops', __name__)

@trade_ops.route('/trades', methods=['POST'])
def create_trade_route():
    data = request.get_json()
    result = create_trade(data)
    return jsonify(result), 201

@trade_ops.route('/trades/<int:trade_id>', methods=['PUT'])
def update_trade_route(trade_id):
    data = request.get_json()
    result = update_trade(trade_id, data)
    return jsonify(result)

@trade_ops.route('/trades/<int:trade_id>', methods=['DELETE'])
def delete_trade_route(trade_id):
    result = delete_trade(trade_id)
    return jsonify(result), 204

@trade_ops.route('/trades/<int:trade_id>', methods=['GET'])
def get_trade_route(trade_id):
    result = get_trade(trade_id)
    return jsonify(result)

@trade_ops.route('/trades', methods=['GET'])
def get_all_trades_route():
    result = get_all_trades()
    return jsonify(result)

app = Flask(__name__)
app.register_blueprint(trade_ops, url_prefix='/api')

if __name__ == '__main__':
    from os import environ
    app.run(host=environ.get('HOST', '127.0.0.1'), port=environ.get('PORT', 5000))