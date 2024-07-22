from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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
    if request.is_json:
        request.data = request.get_json()

@app.route('/trades', methods=['POST'])
def add_trade():
    data = request.data
    trade = Trade(symbol=data['symbol'], volume=data['volume'], price=data['price'])
    db.session.add(trade)
    db.session.commit()
    
    return jsonify(trade.to_json()), 201

@app.route('/trades', methods=['GET'])
def get_trades():
    trades = Trade.query.all()
    return jsonify([trade.to_json() for trade in trades]), 200

@app.route('/trades/<int:id>', methods=['GET'])
def get_trade(id):
    trade = Trade.query.get_or_404(id)
    return jsonify(trade.to_json()), 200

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('APP_PORT', 5000))