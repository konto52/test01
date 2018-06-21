from flask import Flask, render_template, request
from vsearch import search4letters


app = Flask(__name__)


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    pharse = request.form['pharse']
    letters = request.form['letters']
    title = 'Oto Twoje wyniki:'
    results = str(search4letters(pharse,letters))
    return render_template('results.html',
                            the_title = title,
                            the_pharse = pharse,
                            the_letters = letters,
                            the_results = results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Witamy na stronie internetowej search4letters!')

app.run(debug=True)
