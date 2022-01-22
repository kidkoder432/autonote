import autonote as an
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['POST'])
def extract():

    text = request.form['text'].split('\r\n')
    print(text)
    notes = an.extract(text)
    print(notes)
    return render_template('index.html', notes=notes)

app.run('localhost', 5000)