from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def ShowMainPage():
    return

if __name__ == "__main__":
    app.run()