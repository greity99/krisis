#import modules
from bottle import run, template, route, static_file, request, redirect, error
#import psycopg2

#General variables
'''
#Databas
host = "pgserver.mau.se"
database = "XXX"
user = "XXX"
password = "XXX"
port = "5432"  # Default PostgreSQL port
'''


@route("/")
def index():
    """
    Returnar startsidan. 

    Returns:
    template: index
    """
    return template("index")

@route("/Krishantering")
def chrisis_tips():
    return template("chrisis_tips")

@route("/Ny")
def publish_post():
    return template("publish_post")

@route("/Kontakt")
def login():
    return template("contact")

@route("/Logga in")
def login():
    return template("login")

'''
#Connect to PostgreSQL
try: 
    conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port  
    )

    #Open a cursor
    #The cursor is needed to perform database operations
    cur = conn.cursor()
    
except psycopg2.Error as error: 
    print(f"Error: unable to connect to the database\n {error}")
'''

@route("/static/<filename>")
def static_files(filename):
    """
    Funktion vilken returnerar statiska filer (ex. CSS) från mappen static.
    """
    return static_file(filename, root="static")

run(host="127.0.0.1", port=8080)