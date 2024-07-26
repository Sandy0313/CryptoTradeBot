from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TradeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    executed_price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "volume": self.volume,
            "price": self.executed_price
        }

@app.before_request
def validate_json_request():
    if not request.is_json:
        return make_response(jsonify({"error": "Bad request, JSON required"}), 400)
    request.parsed_data = request.get_json()

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": "Bad request"}), 400

@app.errorhandler(500)
def internal_server_error_handler(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/trades', methods=['POST'])
def create_trade_record():
    try:
        trade_data = request.parsed_data
        if not all(key in trade_data for key in ['symbol', 'volume', 'price']):
            return jsonify({"error": "Missing field(s). Required: [symbol, volume, price]"}), 400
        
        new_trade = TradeRecord(symbol=trade_data['symbol'], volume=trade_data['volume'], executed_price=trade_data['price'])
        db.session.add(new_trade)
        db.session.commit()
    except SQLAlchemyError as e:
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "Failed to add trade record, database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error occurred: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify(new_trade.to_dict()), 201

@app.route('/trades', methods=['GET'])
def fetch_all_trades():
    try:
        trade_records = TradeRecord.query.all()
    except SQLAlchemyError as e:
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "Failed to fetch trade records, database error"}), 500
    return jsonify([record.to_dict() for record in trade_records]), 200

@app.route('/trades/<int:trade_id>', methods=['GET'])
def fetch_trade_by_id(trade_id):
    try:
        trade_record = TradeRecord.query.get_or_404(trade_id)
    except SQLAlchemyError as e:
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({"error": "Failed to fetch trade record, database error"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error occurred while fetching trade record with id {trade_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify(trade_record.to_dict()), 200

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('APP_PORT', 5000))