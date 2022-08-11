from importlib.metadata import requires
from flask import jsonify, request
from flask_restx import Resource, Namespace, fields, reqparse
from sqlalchemy import create_engine
import json

from src.database.config import *

DATABASE = {"data": "아무튼 빅-데이터"}

database = create_engine(DB_URL, encoding='utf8', max_overflow=0)

User = Namespace(
    name="User",
    description="from database get user data",
)

user_fields = User.model('User', {  # Model 객체 생성
    'data': fields.String(description='key', required=True, example="님이 적은 것")
})

@User.route('/get-all-data')
class UserTest(Resource):
    def get(self):
        """모든 user의 데이터 받아옴"""

        row = database.execute("""
            select *
            from users
        """).fetchall()

        return jsonify([ {'id': data['id'], 'pw': data['pw']} for data in row ])


get_parser = reqparse.RequestParser()
get_parser.add_argument('col', type=str, required=True ,help='데이터베이스에서 검색할 값이 있는 열')
get_parser.add_argument('data', type=str, required=True ,help='데이터베이스에서 검색할 값')

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=str, required=True ,help="데이터베이스에서 변경하고자 하는 유저의, 아이디")
put_parser.add_argument('col', type=str, required=True ,help='데이터베이스에서 변경할 값이 있는 열')
put_parser.add_argument('data', type=str, required=True ,help='데이터베이스에서 변경할 값')

@User.route('/')
class UserData(Resource):
    @User.doc(
        parser=get_parser,
        responses={
            200: 'Success',
            400: 'Not in database'
        })
    def get(self):
        """column에 해당 값이 있을 경우 가져옴"""
        col = request.args['col']
        arg = f'{request.args["data"]}'
        arg = f'"{arg}"'
        
        try:
            row = database.execute(f"""
                select *
                from users 
                where {col}={arg}
            """).fetchone()
        except:
            return {'search-col': f'{col}', 'search-data': 'None'}, 400

        try:
            return {'search-col': f'{col}', 'search-data': dict([ (key, row[key]) for key in row.keys()])}, 200
        except:
            return {'search-col': f'{col}', 'search-data': 'None'}, 400


    @User.doc(
        parser=put_parser,
        responses={
            200: 'Success',
            400: 'Not in database',
            401: 'Cant change value'
        })
    def put(self):
        """id를 제외한 값들 업데이트 가능"""
        args = request.args
        col = args['col']

        if col=="id":
            return 401

        user_id = request.args['id']
        arg = request.args['data']
        

        database.execute(f"""
            UPDATE users
            SET {col}='{arg}'
            WHERE id='{user_id}'
        """)
        return {'data':'asdf'}
        
        