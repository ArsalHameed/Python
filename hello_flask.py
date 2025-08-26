from flask import Flask, render_template, request
from vfinalsearch import search4letters

app = Flask(__name__)

@app.route("/")   # This maps the root URL (http://127.0.0.1:5001/) to the function
def hello() -> str:
    return "hello world from Flask!"

@app.route('/search4', methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    
    the_title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    
    return render_template(
        'results.html',
        the_title=the_title,
        the_results=results,
        the_letters=letters,
        the_phrase=phrase,
    )

@app.route('/entry')
def entry_page() -> 'html':
    return render_template(
        'entry.html',
        the_title='Welcome to search4letters on the web!'
    )

if __name__ == "__main__":
    app.run(port=5001, debug=True)
