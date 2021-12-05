from datetime import datetime
import difflib


from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///check_text.db'


db = SQLAlchemy(app)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)


class Texts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.String(50), nullable = False, default = datetime.utcnow())
    unique = db.Column(db.Integer, nullable = False)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))


@app.route('/')
@app.route('/texts/')
def texts():
    texts = Texts.query.order_by(Texts.date.desc()).all() #get all texts, order by date
    authors = Authors.query.all() #get all authors, order by id

    return render_template('texts.html', texts = texts, authors = authors)


@app.route('/authors/')
def authors():
    authors = Authors.query.all() #get all authors, order by id

    return render_template('authors.html', authors = authors)


@app.route('/author/<int:id>')
def author(id):
    author = Authors.query.get(id) #get author
    texts = Texts.query.filter(Texts.author_id == id).all() #get all the texts of the author 

    return render_template('author.html', author = author, texts = texts)


@app.route('/text/<int:id>')
def text(id):
    text = Texts.query.get(id) #get text

    return render_template('text.html', text = text)


@app.route('/about/')
def about():
    return render_template('about.html')


def is_exist_author(name):
    authors = Authors.query.all()
    for author in authors:
        if name == author.name:
            return True
    return False


def originality_rating(new_text):
    texts = Texts.query.all()
    maximum_score = 0

    for text in texts:
        current_scope = difflib.SequenceMatcher(None, text.text, new_text).ratio()
        if current_scope > maximum_score:
            maximum_score = current_scope
    
    return maximum_score


@app.route('/check_text/', methods=['POST', 'GET'])
def check_text():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        text = request.form['text']


        if not is_exist_author(author):
            authors = Authors(name=author)

            try:
                db.session.add(authors)
            except:
                return "Error"
        
        
        originality_scope = originality_rating(text)

        if originality_scope > 0.9:
            return "This text is already on the site "
        else:
            author_id = Authors.query.filter(Authors.name == author).first().id #get the author ID 

            texts = Texts(title = title, text = text, unique = round(originality_scope, 2), author_id = author_id)

            try:
                db.session.commit()
                db.session.add(texts)
                db.session.commit()

                return redirect('/texts/')
            except:
                return "Error"

    else:
        return render_template('check_text.html')


if __name__=='__main__':
    app.run(debug=True)
