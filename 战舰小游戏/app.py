import flask
from flask.templating import render_template


app = flask.Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/game_new')
def game_new():
    return render_template('game.new.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)