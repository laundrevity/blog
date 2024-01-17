from flask import Flask, render_template
import markdown2


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/article/<article_name>", methods=["GET"])
def article(article_name: str):
    with open(f"articles/{article_name}.md", "r") as f:
        content = markdown2.markdown(f.read())

    print(f"{content=}")
    return render_template("article.html", content=content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
