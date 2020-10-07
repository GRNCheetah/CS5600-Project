from flask import Blueprint, Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    try:
        if request.method == "POST":
            # Do calcs on answers starting here
            answer1 = request.form['1']
            print(answer1)
        return render_template("quiz.html")
    except Exception as e:
        print("error")
        return render_template("quiz.html", error="something")


        

    

@app.route("/data")
def data():
    return render_template("data.html")

if __name__ == '__main__':
    app.run(debug=True)
