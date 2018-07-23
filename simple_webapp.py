from flask import Flask, session

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Witaj, świecie, tu prosta apka webowa'

@app.route('/page1')
def page1():
    if not check_logged_in():
        return 'Nie jesteś zalogowany. Go away.'
    return 'To jest strona 1.'

@app.route('/page2')
def page2():
    return 'To jest strona 2.'

@app.route('/page3')
def page3():
    return 'To jest strona 3.'

@app.route('/login')
def login() -> str:
    session['logged_in']=True
    return 'Teraz jesteś zalogowany.'

@app.route('/logout')
def logout() -> str:
    if 'logged_in' in session:
        session.pop('logged_in')
        return 'Teraz jesteś wylogowany.'
    return 'Już jesteś wylogowany.'

@app.route('/status')
def status() -> str:
    if 'logged_in' in session:
        return 'status: zalogowany'
    return 'status: niezalogowany'

def check_logged_in() -> bool:
    if 'logged_in' in session:
        return True
    return False

app.secret_key = 'HUbbsidbs88dy7sd8t7^%4efvh3vW'

if __name__ == '__main__':
    app.run(debug=True)
