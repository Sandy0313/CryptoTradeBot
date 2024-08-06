from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    new_trade = Trade(symbol=data['symbol'], volume=data['volume'], price=data['price'], date=data['date'])
    db.session.add(new_trade)
    db.session.commit()
    return jsonify(new_trade.to_dict()), 201

@app.route('/trades', methods=['GET'])
def get_trades():
    trades = Trade.query.all()
    return jsonify([trade.to_dict() for trade in trades])

@app.route('/trade/<int:id>', methods=['GET'])
def get_trade(id):
    trade = Trade.query.get_or_404(id)
    return jsonify(trade.to_dict())

@app.route('/trade/<int:id>', methods=['PUT'])
def update_trade(id):
    trade = Trade.query.get_or_404(id)
    data = request.get_json()
    trade.symbol = data['symbol']
    trade.volume = data['volume']
    trade.price = data['price']
    trade.date = data['date']
    db.session.commit()
    return jsonify(trade.to_dict())

@app.route('/trade/<int:id>', methods=['DELETE'])
def delete_trade(id):
    trade = Trade.query.get_or_404(id)
    db.session.delete(trade)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)