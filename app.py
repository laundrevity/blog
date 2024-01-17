from flask import Flask, render_template
import markdown2
import os


app = Flask(__name__)


def get_article_names():
    articles = []
    for filename in os.listdir("articles/"):
        if filename.endswith(".md"):
            article_title = filename[:-3]  # remove the .md extension
            article_title = article_title[0].upper() + article_title[1:]
            article_title = article_title.replace("_", " ")
            articles.append(article_title)
    return articles


@app.context_processor
def inject_articles():
    return {"articles": get_article_names()}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/article/<article_name>", methods=["GET"])
def article(article_name: str):
    filename = article_name.lower().replace(" ", "_")

    with open(f"articles/{filename}.md", "r") as f:
        content = markdown2.markdown(f.read())

    return render_template("article.html", content=content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
