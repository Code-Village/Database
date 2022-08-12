import os
from dotenv import load_dotenv
from flask import Flask
from flask_restx import Api, Resource, reqparse

from src.database.api.user import *
from src.database.api.team import *

load_dotenv()

app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'


api = Api(
    app,
    version=0.1, 
    title="Code Village - DB", 
    description="API for {Code Village}", 
    terms_url="/",
    contact="gkstkdgus821@gmail.com", 
    license='BSD 3-Clause "New" or "Revised" License'
)

api.add_namespace(User, '/user')
api.add_namespace(Team, '/team')

if __name__ == "__main__":
    # port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=5000, debug=True)