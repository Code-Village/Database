from importlib.metadata import requires
from flask import jsonify, request
from flask_restx import Resource, Namespace, fields, reqparse
from sqlalchemy import create_engine
from datetime import datetime

from src.database.config import *

database = create_engine(DB_URL, encoding='utf8', max_overflow=0)

Team = Namespace(
    name="Team",
    description="from database get team data",
)

get_user_data_parser = reqparse.RequestParser() # 대부분 id, 닉네임 검색
get_user_data_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 검색할 값')

post_user_data_parser = reqparse.RequestParser()
post_user_data_parser.add_argument('teamname', type=str, required=True, help='가입할 유저의 id')
post_user_data_parser.add_argument('admin', type=str, required=True, help='가입할 유저의 pw')

@Team.route('/regist') # 팀 생성시 이용
class TeamRegist(Resource):
    @Team.doc(
    parser=get_user_data_parser,
    responses={
        200: 'Can regist',
        401: 'Failed To Append Team',
        402: 'Failed To Append Teamlist'
    })
    def get(self):
        """params 필요. 해당 params가 있는 것만 검색 -> 중복 방지용. 팀 이름 중복 검사에 사용"""
        args = request.args
        
        query = f"SELECT COUNT(IF(tname='{args['data']}',1,NULL)) as cnt FROM teams"
        row = database.execute(query).fetchone()

        if row[0] > 0:
            return 201
        else:
            return 200

    @Team.doc(
    parser=post_user_data_parser,
    responses={
        200: 'Can regist',
        201: 'Duplicate Data in Database',
        400: 'Fatal error',
    })
    def post(self):
        """teamname, 팀장 이름을 데이터베이스에 전달"""

        args = request.args

        teamname = args['teamname']
        tadmin_nickname = args['admin']

        try:
            query = f"INSERT INTO teams (tname, tadmin, tfounded) VALUES ('{teamname}', '{tadmin_nickname}', '{datetime.today()}');"
            database.execute(query)
        except:
            return 402

        try:
            query = f"INSERT INTO companys (tname, uname) VALUES ('{teamname}', '{tadmin_nickname}')"
            database.execute(query)
        except:
            return 401

        return 200

get_parser = reqparse.RequestParser()
get_parser.add_argument('teamname', type=str, required=True, help='팀 이름')

post_parser = reqparse.RequestParser()
post_parser.add_argument('teamname', type=str, required=True, help="팀 이름")
post_parser.add_argument('uname', type=str, required=True, help="팀원 닉네임")

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=str, required=True, help="데이터베이스에서 변경하고자 하는 팀의, 이름")
put_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 변경할 값이 있는 열')
put_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 변경할 값')

del_parser = reqparse.RequestParser()
del_parser.add_argument('teamname', type=str, required=True, help='데이터베이스에서 삭제할 팀 이름')

@Team.route('')
class TeamData(Resource):
    @Team.doc(
        parser=get_parser,
        responses={
            200: 'Success',
            400: 'Fatal error',
            401: 'Not in database'
        })
    def get(self):
        """teamname에 해당 값이 있을 경우 가져옴"""
        arg = request.args["teamname"]
        
        try:
            row = database.execute(f"""
                select *
                from teams 
                where tname='{arg}';
            """).fetchone()
        except:
            return 400


        if row == None:
            return 401

        ret_dict = dict([ (key, row[key]) for key in row.keys() ])
        ret_dict['tfounded'] = ret_dict['tfounded'].strftime("%Y-%m-%d")
        
        return ret_dict, 200

    @Team.doc(
        parser=post_parser,
        responses={
            200: 'Success',
            400: 'Fatal error'
        }
    )
    def post(self):
        """유저를 팀에 추가"""
        args = request.args

        tname = args['teamname']
        uname = args['uname']

        query = f"INSERT INTO companys (tname, uname) VALUES ('{tname}', '{uname}')"
        try:
            database.execute(query)
        except:
            return 400

        return 200


    @Team.doc(
        parser=put_parser,
        responses={
            200: 'Query succeed',
            400: 'Fatal error'
        })
    def put(self):
        """id를 제외한 값들 업데이트 가능"""
        args = request.args
        col = args['col']

        if col=="id":
            return 401

        user_id = request.args['id']
        arg = request.args['data']
        
        try:
            database.execute(f"""
                UPDATE teams
                SET {col}='{arg}'
                WHERE id='{user_id}'
            """)

            
        except:
            return 400

        return 200

    @Team.doc(
        parser=del_parser,
        responses={
            200: 'Query succeed',
            400: 'Fatal error'
        })
    def delete(self):
        """해당 teamname을 가진 팀 삭제"""
        team_name = request.args['teamname']

        try:
            database.execute(f"""
                DELETE
                FROM teams
                WHERE tname='{team_name};'
            """)
        except:
            return 400
        return 200