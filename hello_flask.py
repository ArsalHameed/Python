from flask import Flask
from vfinalsearch import search4letters
app = Flask(__name__)

@app.route("/")   # This maps the root URL (http://127.0.0.1:5001/) to the function
def hello() -> str:
    return "hello world from Flask!"

@app.route('/search4')
def do_search()-> str:
    return str(search4letters('life, the universe, and everything','eiru,!'))

if __name__ == "__main__":
    app.run(port=5001)
