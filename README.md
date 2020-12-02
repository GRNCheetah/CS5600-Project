# CS5600-Project

## Running the Flask Application

Install `flask` if necessary:

`$ pip install flask`
`$ pip install flask_sqlalchemy`
`$ pip install flask_login`

Simply run the application from the command line:

`$ python server.py`

Navigate to `localhost:5000` in your browser to view the application

## Setting up the Database

To set up empty databases (`database.db` and `users.db`), rerun

`$ python init_db.py`

The database files will be updated when clients use the application.
