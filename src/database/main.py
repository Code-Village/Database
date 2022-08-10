import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

load_dotenv()


def createApp():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    print(app.config)

    database = create_engine(app.config['DB_URL'], encoding='utf8', max_overflow=0)
    app.database = database

    @app.route("/")
    def main():
        return {"hello": "world!"}


    @app.route("/user")
    def user():
        return {"name": "main"}

    @app.route("/db")
    def db():
        row = app.database.execute("""
            select *
            from users
        """).fetchall()

        for data in row:
            print(type(data['id']))

        return jsonify([ {'id': data['id'], 'pw': data['pw']} for data in row ])

    return app



if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    createApp().run(host="0.0.0.0", port=port, debug=True)