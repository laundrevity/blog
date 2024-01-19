from flask import Flask, render_template, request
from logging.handlers import RotatingFileHandler
from markdown2 import Markdown
import logging
import re
import os


app = Flask(__name__)
markdowner = Markdown(extras=["fenced-code-blocks"])

# Configure Rotating File Handler
file_handler = RotatingFileHandler("app.log", maxBytes=10_000_000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
    )
)

# Configure Stream Handler for stdout
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))

# Add handlers to the Flask app's logger
app.logger.addHandler(file_handler)
app.logger.addHandler(stream_handler)

gunicorn_error_logger = logging.getLogger("gunicorn.error")
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)


@app.before_request
def log_request_info():
    app.logger.info(
        f"Remote Addr: {request.remote_addr}, Request: {request.method} {request.url}"  # , Agent: {request.user_agent}"
    )


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
    math_sections = []

    with open(f"articles/{filename}.md", "r") as f:
        content = f.read()

        # Extract math sections
        def replace_math(m):
            math_sections.append(m.group(0))
            return f"<!--MATH{len(math_sections)-1}-->"

        content = re.sub(r"(\$\$[\s\S]+?\$\$|\$[^$]*\$)", replace_math, content)

        # convert markdown to HTML
        content = markdowner.convert(content)

        # reinsert math sections
        for i, math in enumerate(math_sections):
            content = content.replace(f"<!--MATH{i}-->", math)

    return render_template("article.html", content=content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
