from flask import Flask, Response

app = Flask(__name__)


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"


@app.route("/favicon.ico")
def favicon() -> Response:
    return app.send_static_file("favicon.ico")


if __name__ == "__main__":
    app.run()
