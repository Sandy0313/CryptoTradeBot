from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
import logging
from datetime import datetime
import sys
from flask_caching import Cache  # Import the Cache class

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', 'sqlite:///trades.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'SimpleCache'  # Choose the cache type, simple for development
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Default cache timeout is 300 seconds (5 minutes)
cache = Cache(app)

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'volume': self.volume,
            'price': self.price,
            'date': self.date.isoformat()
        }

@app.route('/trade', methods=['POST'])
def create_trade():
    data = request.get_json()
    try:
        new_trade = Trade(symbol=data['symbol'], volume=data['volume'], price=data['price'], date=datetime.fromisoformat(data['date']))
        db.session.add(new_trade)
        db.session.commit()
        logger.info(f'New trade created: {new_trade.to_dict()}')
        return jsonify(new_trade.to_dict()), 201
    except Exception as e:
        logger.error(f'Error creating trade: {e}')
        return jsonify({"error": "Error creating trade"}), 400

@app.route('/trades', methods=['GET'])
@cache.cached(timeout=60, query_string=True)  # Cache this view for 60 seconds and consider the query string when caching
def get_trades():
    trades = Trade.query.all()
    logger.info('Fetched all trades')
    return jsonify([trade.to_dict() for trade in trades])

@app.route('/trade/<int:id>', methods=['GET'])
@cache.cached(timeout=120, key_prefix='trade_%s')  # Cache for 2 minutes and use the trade ID for a unique key prefix
def get_trade(id):
    trade = Trade.query.get_or_404(id)
    logger.info(f'Trade fetched: {trade.to_dict()}')
    return jsonify(trade.to_dict())

@app.route('/trade/<int:id>', methods=['PUT'])
def update_trade(id):
    trade = Trade.query.get_or_404(id)
    data = request.get_json()
    trade.symbol = data['symbol']
    trade.volume = data['volume']
    trade.price = data['price']
    trade.date = datetime.fromisoformat(data['date'])
    db.session.commit()
    logger.info(f'Trade updated: {trade.to_dict()}')
    # Invalidate the cache for the updated trade
    cache.delete_memoized(get_trade, id)
    return jsonify(trade.to_dict())

@app.route('/trade/<int:id>', methods=['DELETE'])
def delete_trade(id):
    trade = Trade.query.get_or_404(id)
    db.session.delete(trade)
    db.session.commit()
    logger.info(f'Trade deleted: id {id}')
    # Invalidate the cache for the deleted trade
    cache.delete_memoized(get_trade, id)
    return jsonify({'success': True})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)