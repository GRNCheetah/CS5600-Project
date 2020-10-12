from flask import Blueprint, Flask, render_template, request
app = Flask(__name__)

NUM_QUESTIONS = 50

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    try:
        if request.method == "POST":
            # Do calcs on answers starting here
            answers = []
            for answer in range (1, NUM_QUESTIONS+1):
                if answer==25:
                    answers = answers + (request.form.getlist(str(answer)))
                else:
                    answers.append(request.form[str(answer)])
            print(answers, flush=True)
        return render_template("quiz.html")
    except Exception as e:
        print("error")
        return render_template("quiz.html", error="something")


        

    

@app.route("/data")
def data():
    return render_template("data.html")

if __name__ == '__main__':
    app.run(debug=True)
