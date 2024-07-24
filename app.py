from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "volume": self.volume,
            "price": self.price
        }

@app.before_request
def before_request():
    if not request.is_json:
        return make_response(jsonify({"error": "Bad request, JSON required"}), 400)
    request.data = request.get_json()

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/trades', methods=['POST'])
def add_trade():
    try:
        data = request.data
        if not all(field in data for field in ['symbol', 'volume', 'price']):
            return jsonify({"error": "Missing field(s). Required: [symbol, volume, price]"}), 400
        
        trade = Trade(symbol=data['symbol'], volume=data['volume'], price=data['price'])
        db.session.add(trade)
        db.session.commit()
    except SQLAlchemyError as e:
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "Failed to add trade, database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify(trade.to_json()), 201

@app.route('/trades', methods=['GET'])
def get_trades():
    try:
        trades = Trade.query.all()
    except SQLAlchemyError as e:
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "Failed to fetch trades, database error"}), 500
    return jsonify([trade.to_json() for trade in trades]), 200

@app.route('/trades/<int:id>', methods=['GET'])
def get_trade(id):
    try:
        trade = Trade.query.get_or_404(id)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "Failed to fetch trade, database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error occurred while fetching trade with id {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify(trade.to_json()), 200

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('APP_PORT', 5000))