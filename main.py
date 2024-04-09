#import modules
from bottle import run, template, route
import route, run, template, static_file, request, redirect
import psycopg2
 
'''
#General variables
host = "pgserver.mau.se"
database = "XXX"
user = "XXX"
password = "XXX"
port = "5432"  # Default PostgreSQL port
'''


@route("/")
def index():
    return template("index.html")

@route("/Kristips")
def chrisis_tips():
    return template("chrisis_tips.html")

@route("/Skapa inlägg")
def publish_post():
    return template("publish_post.html")

@route("/logga in")
def login():
    return template("login.html")

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

run(host="127.0.0.1", port=8080)