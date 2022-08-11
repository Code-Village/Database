from flask import jsonify
from flask_restx import Resource, Namespace, fields
from sqlalchemy import create_engine

from src.database.config import *

DATABASE = {"data": "아무튼 빅-데이터"}

database = create_engine(DB_URL, encoding='utf8', max_overflow=0)

User = Namespace(
    name="User",
    description="테스트를 위해 작성한 API.",
)

user_fields = User.model('User', {  # Model 객체 생성
    'data': fields.String(description='key', required=True, example="님이 적은 것")
})

@User.route('')
class UserTest(Resource):
    def get(self):
        row = database.execute("""
            select *
            from users
        """).fetchall()

        return jsonify([ {'id': data['id'], 'pw': data['pw']} for data in row ])

@User.route('/<string:id>')
class UserData(Resource, id):
    def get(self):
        row = database.execute(f"""
            select {id}
            from users
        """).fetchone()
        
        return jsonify([ {'id': data['id'], 'pw': data['pw']} for data in row ])
