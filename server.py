from flask import Blueprint, Flask, render_template, request, Response
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import pandas as pd
import collections
import io
app = Flask(__name__)

NUM_QUESTIONS = 50

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/summary_plot.png')
def plot_summary_png():
    fig = update_summary_graph()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/EI_plot.png')
def plot_EI_png():
    fig = update_trait_graph()[0]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/SN_plot.png')
def plot_SN_png():
    fig = update_trait_graph()[1]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/TF_plot.png')
def plot_TF_png():
    fig = update_trait_graph()[2]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/JP_plot.png')
def plot_JP_png():
    fig = update_trait_graph()[3]
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def update_summary_graph():
    # Retrieve all submission data from database.
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()

    # Data currently stored in two different methods for data calculations.
    summary = {
        'Extrovert': 0,
        'Introvert': 0,
        'Sensor': 0,
        'Intuitive': 0,
        'Thinker': 0,
        'Feeler': 0,
        'Judger': 0,
        'Perceiver': 0,
    }
    df = pd.DataFrame(columns=['Extrovert', 'Introvert', 'Sensor', 'Intuitive', 'Thinker', 'Feeler', 'Judger', 'Perceiver'])

    # Store aggregate database data.
    for i in range(0, len(posts)):
        summary['Extrovert'] += posts[i]['sumE']
        summary['Introvert'] += posts[i]['sumI']
        summary['Sensor'] += posts[i]['sumS']
        summary['Intuitive'] += posts[i]['sumN']
        summary['Thinker'] += posts[i]['sumT']
        summary['Feeler'] += posts[i]['sumF']
        summary['Judger'] += posts[i]['sumJ']
        summary['Perceiver'] += posts[i]['sumP']
        new_row = { 'Extrovert': posts[i]['sumE'],
                    'Introvert': posts[i]['sumI'],
                    'Sensor':    posts[i]['sumS'],
                    'Intuitive': posts[i]['sumN'],
                    'Thinker':   posts[i]['sumT'],
                    'Feeler':    posts[i]['sumF'],
                    'Judger':    posts[i]['sumJ'],
                    'Perceiver': posts[i]['sumP'] }
        df = df.append(new_row, ignore_index=True)

    # Sort trait sums in ascending order.
    summary = collections.OrderedDict(sorted(summary.items(), key=lambda kv: kv[1]))

    # Generate `Trait Distribution` graph.
    colors = []
    for val in summary.keys():
        if val == 'Extrovert' or val == 'Introvert':
            colors.append('blue')
        elif val == 'Sensor' or val == 'Intuitive':
            colors.append('green')
        elif val == 'Thinker' or val == 'Feeler':
            colors.append('red')
        elif val == 'Judger' or val == 'Perceiver':
            colors.append('orange')

    fig = Figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(summary.keys(), summary.values(), width=0.8, color=colors)
    ax.set_xlabel('Trait', fontsize=14)
    ax.set_ylabel('Total Trait Sum', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=13)
    fig.suptitle('Individual Trait Distribution', fontsize=16)

    return fig


def update_trait_graph():
    # Retrieve all submission data from database.
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()

    # Data currently stored in two different methods for data calculations.
    traits = {
        'Extrovert': 0,
        'Introvert': 0,
        'Sensor': 0,
        'Intuitive': 0,
        'Thinker': 0,
        'Feeler': 0,
        'Judger': 0,
        'Perceiver': 0,
    }
    # Store aggregate database data.
    for i in range(0, len(posts)):
        if(posts[i]['personalityType'][0] == 'E'):
            traits['Extrovert'] += 1
        else:
            traits['Introvert'] += 1
        if(posts[i]['personalityType'][1] == 'S'):
            traits['Sensor'] += 1
        else:
            traits['Intuitive'] += 1
        if(posts[i]['personalityType'][2] == 'T'):
            traits['Thinker'] += 1
        else:
            traits['Feeler'] += 1
        if(posts[i]['personalityType'][3] == 'J'):
            traits['Judger'] += 1
        else:
            traits['Perceiver'] += 1

    trait_sets = [['Extrovert', 'Introvert'], ['Sensor', 'Intuitive'], ['Thinker', 'Feeler'], ['Judger', 'Perceiver']]
    figures = []
    
    # Construct graph for each trait
    for subset in trait_sets:
        traits_subset = {key: traits[key] for key in subset}
        fig = Figure(figsize=(10, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.barh(list(traits_subset.keys()), list(traits_subset.values()), height=0.8)
        ax.set_xlabel('Trait Sum', fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=13)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.suptitle(subset[0] + ' vs ' + subset[1], fontsize=16)
        figures.append(fig)

    return figures


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

            # Calculate sums for each trait
            result = {
                "sumE": 0,
                "sumI": 0,
                "sumS": 0,
                "sumN": 0,
                "sumT": 0,
                "sumF": 0,
                "sumJ": 0,
                "sumP": 0,
                "personalityType": ""
            }
            for answer in answers:
                if answer[0] == 'E':
                    result["sumE"] += int(answer[-1])
                elif answer[0] == 'I':
                    result["sumI"] += int(answer[-1])
                elif answer[0] == 'S':
                    result["sumS"] += int(answer[-1])
                elif answer[0] == 'N':
                    result["sumN"] += int(answer[-1])
                elif answer[0] == 'T':
                    result["sumT"] += int(answer[-1])
                elif answer[0] == 'F':
                    result["sumF"] += int(answer[-1])
                elif answer[0] == 'J':
                    result["sumJ"] += int(answer[-1])
                elif answer[0] == 'P':
                    result["sumP"] += int(answer[-1])
            #print('Sums are: ', sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, flush=True)


            if(result["sumI"] >= result["sumE"]):
                result["personalityType"] += "I"
            else:
                result["personalityType"] += "E"
            if(result["sumN"] >= result["sumS"]):
                result["personalityType"] += "N"
            else:
                result["personalityType"] += "S"
            if(result["sumT"] >= result["sumF"]):
                result["personalityType"] += "T"
            else:
                result["personalityType"] += "F"
            if(result["sumP"] >= result["sumJ"]):
                result["personalityType"] += "P"
            else:
                result["personalityType"] += "J"

            # Send to database
            conn = get_db_connection()
            conn.execute("INSERT INTO submissions (sumE, sumI, sumS, sumN, sumT, sumF, sumJ, sumP, personalityType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (result["sumE"], result["sumI"], result["sumS"], result["sumN"], result["sumT"], result["sumF"], result["sumJ"], result["sumP"], result["personalityType"]))
            conn.commit()
            conn.close()
            return render_template("results.html", user_result=result)
        else:
            return render_template("quiz.html")
    except Exception as e:
        print("error:", e)
        return render_template("quiz.html", error="something")


@app.route("/results")
def results(data=None):
    return render_template("results.html", user_result={})


@app.route("/data")
def data():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM submissions').fetchall()
    conn.close()
    return render_template("data.html", posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
