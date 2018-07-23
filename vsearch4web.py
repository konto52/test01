from flask import Flask, render_template, request, escape
from vsearch import search4letters

from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': 'localhost',
                          'user': 'vsearch',
                          'password': 'vsearchpasswd',
                          'database': 'vsearchlogDB',}


def log_request_file(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')


def log_request(req: 'flask request', res: str) -> None:
    """Funkcja logująca do bazy danych mysql"""

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """INSERT INTO log
           (pharse, letters, ip , browser_string, results)
            VALUES
           (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['pharse'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res, ))
        
    
@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    pharse = request.form['pharse']
    letters = request.form['letters']
    title = 'Oto Twoje wyniki:'
    results = str(search4letters(pharse,letters))
#    log_request_file(request,results)
    log_request(request,results)
    return render_template('results.html',
                            the_title = title,
                            the_pharse = pharse,
                            the_letters = letters,
                            the_results = results,)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Witamy na stronie internetowej search4letters!')

@app.route('/viewlog_file')
def view_the_log_file() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Dane z formularza', 'Adres klienta', "Agent_uzytkownika")
    return render_template('viewlog.html',
                           the_title = 'Widok logu',
                            the_row_titles = titles,
                            the_data = contents,)

@app.route('/viewlog')
def view_the_log() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select pharse, letters, ip, browser_string, results
                  from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = ('Fraza', 'Litery', 'Adres klienta', 'Agent użytkownika', 'Wynik')
        return render_template('viewlog.html',
                               the_title='Widok logu',
                               the_row_titles=titles,
                               the_data=contents,)



if __name__ == '__main__':
    app.run(debug=True)
