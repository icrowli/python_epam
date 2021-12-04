from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/texts/')
def texts():
    return render_template('texts.html')


@app.route('/authors/')
def authors():
    return render_template('authors.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/check_text/')
def check_text():
    return render_template('check_text.html')


if __name__=='__main__':
    app.run(debug=True)
