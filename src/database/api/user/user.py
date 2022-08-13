from importlib.metadata import requires
from flask import jsonify, request
from flask_restx import Resource, Namespace, fields, reqparse
from sqlalchemy import create_engine

from src.database.config import *

database = create_engine(DB_URL, encoding='utf8', max_overflow=0)

User = Namespace(
    name="User",
    description="from database get user data",
)

user_fields = User.model('User', {  # Model 객체 생성
    'data': fields.String(description='key', required=True, example="님이 적은 것")
})

get_user_data_parser = reqparse.RequestParser() # 대부분 id, 닉네임 검색
get_user_data_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 검색할 값이 있는 열')
get_user_data_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 검색할 값')

post_user_data_parser = reqparse.RequestParser()
post_user_data_parser.add_argument('id', type=str, required=True, help='가입할 유저의 id')
post_user_data_parser.add_argument('pw', type=str, required=True, help='가입할 유저의 pw')
post_user_data_parser.add_argument('nickname', type=str, required=True, help='가입할 유저의 닉네임')
post_user_data_parser.add_argument('avartar', type=int, required=True, help='가입할 유저의 아바타 번호')

@User.route('/regist') # 회원가입시 이용
class UserRegist(Resource):
    @User.doc(
    parser=get_user_data_parser,
    responses={
        200: 'Can regist',
        201: 'Duplicate Data in Database',
    })
    def get(self):
        """params 필요. 해당 params가 있는 것만 검색 -> 중복 방지용. id,nickname 중복 검사에 사용"""
        args = request.args

        col = args['col']
        data = args['data']
        
        query = f"SELECT COUNT(IF({col}='{data}',1,NULL)) as cnt FROM users"
        rows = [ list(row) for row in database.execute(query).fetchall() ]

        if rows[0][0] > 0:
            return 201
        else:
            return 200

    @User.doc(
    parser=post_user_data_parser,
    responses={
        200: 'Can regist',
        201: 'Duplicate Data in Database'
    })
    def post(self):
        """id, pw, nickname을 데이터베이스에 전달"""
        args = request.args

        id = args['id']
        pw = args['pw']
        nickname = args['nickname']
        avartar = args['avartar']

        query = f"INSERT INTO users (id, pw, nickname, avartar) VALUES ('{id}', '{pw}', '{nickname}', {avartar});"
        try:
            database.execute(query)
        except:
            return 201

        return 200


get_parser = reqparse.RequestParser()
get_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 검색할 값이 있는 열')
get_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 검색할 값')

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=str, required=True, help="데이터베이스에서 변경하고자 하는 유저의, 아이디")
put_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 변경할 값이 있는 열')
put_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 변경할 값')

del_parser = reqparse.RequestParser()
del_parser.add_argument('id', type=str, required=True, help='데이터베이스에서 삭제할 아이디')

@User.route('')
class UserData(Resource):
    @User.doc(
        parser=get_parser,
        responses={
            200: 'Success',
            201: 'Not in database',
            400: 'Fatal error'
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
            return 400

        try: 
            row.keys()
        except:
            return 201

        ret_data = dict([ (key, row[key]) for key in row.keys() ])
        
        ret = jsonify(ret_data)
        ret.status_code = 200

        return ret


    @User.doc(
        parser=put_parser,
        responses={
            200: 'Query succeed',
            400: 'Fatal error',
            401: 'Cant change values'
        })
    def put(self):
        """id를 제외한 값들 업데이트 가능"""
        args = request.args
        col = args['col']

        if col=="id" or col=="uid":
            return 401

        user_id = request.args['id']
        arg = request.args['data']
        
        try:
            database.execute(f"""
                UPDATE users
                SET {col}='{arg}'
                WHERE id='{user_id}'
            """)
        except:
            return 400

        return 200

    @User.doc(
        parser=del_parser,
        responses={
            200: 'Query succeed',
            400: 'Fatal error'
        })
    def delete(self):
        """해당 id를 가진 계정 삭제"""
        user_id = request.args['id']

        try:
            database.execute(f"""
                DELETE
                FROM users
                WHERE id='{user_id}'
            """)
        except:
            return 400

        return 200