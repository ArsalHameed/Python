from flask import Flask, render_template, request
from markupsafe import escape
from vfinalsearch import search4letters

app = Flask(__name__)

def log_request(req: 'flask_request',res: str) -> None:
    with open('vsearch.log','a') as log:
        print(req.form,req.remote_addr,req.user_agent,res,file=log,sep='|')
 
@app.route('/search4', methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    
    the_title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request,results)
    return render_template(
        'results.html',
        the_title=the_title,
        the_results=results,
        the_letters=letters,
        the_phrase=phrase,
    )
@app.route("/") 
@app.route('/entry')
def entry_page() -> 'html':
    return render_template(
        'entry.html',
        the_title='Welcome to search4letters on the web!'
    )
@app.route('/viewlog')
def view_the_log() -> str:
    with open ('vsearch.log') as log:
        contents = log.read()
        return escape(contents)
if __name__ == "__main__":
    app.run(port=5001, debug=True)
