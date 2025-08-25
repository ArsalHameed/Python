from flask import Flask

app = Flask(__name__)

@app.route("/")   # This maps the root URL (http://127.0.0.1:5001/) to the function
def hello() -> str:
    return "hello world from Flask!"

if __name__ == "__main__":
    app.run(port=5001)
