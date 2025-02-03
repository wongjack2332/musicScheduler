from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    return app


app = create_app()


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/signup")
def signup():
    return "Sign up page"


@app.route("/login")
def login():
    return "Login Page"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
