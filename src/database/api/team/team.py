from importlib.metadata import requires
from flask import jsonify, request
from flask_restx import Resource, Namespace, fields, reqparse
from sqlalchemy import create_engine
from datetime import datetime
import json

from src.database.config import *

database = create_engine(DB_URL, encoding='utf8', max_overflow=0)

Team = Namespace(
    name="Team",
    description="from database get team data",
)

get_user_data_parser = reqparse.RequestParser() # 대부분 id, 닉네임 검색
get_user_data_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 검색할 값')

post_user_data_parser = reqparse.RequestParser()
post_user_data_parser.add_argument('tname', type=str, required=True, help='만들 팀의 이름')
post_user_data_parser.add_argument('admin', type=str, required=True, help='만들 팀의 팀장 닉네임')

@Team.route('/regist') # 팀 생성시 이용
class TeamRegist(Resource):
    @Team.doc(
    parser=get_user_data_parser,
    responses={
        200: 'Can regist',
        201: 'Same Name in Database'
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
        401: 'Cant post data to Company table',
        402: 'Cant post data to Team table'
    })
    def post(self):
        """teamname, 팀장 이름을 데이터베이스에 전달"""

        args = request.args

        teamname = args['tname']
        tadmin_nickname = args['admin']

        try:
            query = f"INSERT INTO teams (tname, tadmin, tfounded) VALUES ('{teamname}', '{tadmin_nickname}', '{datetime.today()}')"
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
get_parser.add_argument('tname', type=str, required=True, help='팀 이름')

post_parser = reqparse.RequestParser()
post_parser.add_argument('tname', type=str, required=True, help="팀 이름")
post_parser.add_argument('uname', type=str, required=True, help="팀원 닉네임")

put_parser = reqparse.RequestParser()
put_parser.add_argument('tname', type=str, required=True, help="데이터베이스에서 변경하고자 하는 팀의, 이름")
put_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 변경할 값이 있는 열')
put_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 변경할 값')

del_parser = reqparse.RequestParser()
del_parser.add_argument('tname', type=str, required=True, help='데이터베이스에서 삭제할 팀 이름')

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
        arg = request.args["tname"]
        
        try:
            row = database.execute(f"""
                select *
                from teams 
                where tname='{arg}'
            """).fetchone()
        except:
            return 400


        if row == None:
            return 401

        ret_dict = dict([ (key, row[key]) for key in row.keys() ])
        ret_dict['tfounded'] = ret_dict['tfounded'].strftime("%Y-%m-%d")

        
        ret = jsonify(ret_dict)
        ret.status_code = 200


        return ret

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

        tname = args['tname']
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
            400: 'Fatal error',
            401: 'Cant change values'
        })
    def put(self):
        """팀장만 변경 가능? 팀 이름도 변경 가능? teamlike, teamview는 항상 올라가야하므로 수정 가능해야함"""
        args = request.args
        col = args['col']

        if col=="tfounded" or col=="tid":
            return 401

        teamname = request.args['tname']
        arg = request.args['data']
        
        try:
            database.execute(f"""
                UPDATE teams
                SET {col}={arg}
                WHERE tname='{teamname}'
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
        team_name = request.args['tname']

        try:
            database.execute(f"""
                DELETE
                FROM teams
                WHERE tname='{team_name}'
            """)
        except:
            return 400
        return 200