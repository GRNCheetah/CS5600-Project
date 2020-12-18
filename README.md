# CS5600-Project

## Running the Flask Application

We will be using Python3

Install `flask` if necessary:

```
$ pip install flask
$ pip install flask_sqlalchemy
$ pip install flask_login
```

Simply run the application from the command line:

`$ python server.py`

Navigate to `localhost:5000` in your browser to view the application

## Running the Quiz Creator

The `radio_gen.py` file will generate the `quiz.html` file from the questions specified in `questions.txt`. Edit the html tags in `radio_gen.py` to how you want it, then run using:

`$ python radio_gen.py`

Replace the old file in `templates/quiz.html`
