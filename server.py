from flask import Blueprint, Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/data")
def data():
    return render_template("data.html")

if __name__ == '__main__':
    app.run(debug=True)
