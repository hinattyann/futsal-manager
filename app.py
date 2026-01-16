import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# DB接続設定（環境変数から読み込む）
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# モデル定義（SQLAlchemy用）
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer)
    position = db.Column(db.String(10))

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(100))
    type = db.Column(db.String(20))

# --- ルーティング（Webページの機能） ---

# 1. トップページ：予定一覧を表示 (Read)
@app.route('/')
def index():
    try:
        schedules = Schedule.query.all()
        results = [
            {
                "id": s.id,
                "date": str(s.date),
                "time": str(s.time),
                "location": s.location,
                "type": s.type
            } for s in schedules
        ]
        return jsonify({"schedules": results})
    except Exception as e:
        return str(e)

# 2. 部員登録機能 (Create)
@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    new_member = Member(
        name=data['name'],
        number=data['number'],
        position=data['position']
    )
    try:
        db.session.add(new_member)
        db.session.commit()
        return jsonify({"message": "Member added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)