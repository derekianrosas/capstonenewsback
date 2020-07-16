from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)

class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    url = db.Column(db.String(), nullable=False)
    urlToImage = db.Column(db.String(), nullable=False)

    def __init__(self, title, description, url, urlToImage):
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage

class NewsArticleSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description","url","urlToImage")

news_article_schema = NewsArticleSchema()
multiple_article_schema = NewsArticleSchema(many=True)

@app.route("/news-article/add-article", methods=["POST"])
def add_article():
    if request.content_type != "application/json":
        return jsonify("Error: data must be sent as JSON")
    
    post_data = request.get_json()
    title = post_data.get("title")
    description = post_data.get("description")
    url = post_data.get("url")
    urlToImage = post_data.get("urlToImage")

    record = NewsArticle(title, description, url, urlToImage)
    db.session.add(record)
    db.session.commit()

    return jsonify("Article added successfully")


@app.route("/news-article/get-articles", methods=["GET"])
def get_all_articles():
    all_articles = db.session.query(NewsArticle).all()
    return jsonify(multiple_article_schema.dump(all_articles))




if __name__ == "__main__":
    app.run(debug=True)