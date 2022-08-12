from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def tester():
    return "Hello!"

@app.route('/test')
def getter():
    res = requests.get(url="https://code-village-db.herokuapp.com/user?col=id&data=gkstkdgus821")
    print(res.json(), type(res.json()))

    return res.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)