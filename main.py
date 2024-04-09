#import modules
from bottle import run, template, route
import route, run, template, static_file, request, redirect
import psycopg2

#General variables
host = "pgserver.mau.se"
database = "XXX"
user = "XXX"
password = "XXX"
port = "5432"  # Default PostgreSQL port



@route("/")
def index():
    return template("index")

@route("/views/krisklar_tips.html")
def chrisis_tips():
    return template("krisklar_tips")

#Denna är lite oklar, vet inte varför det finns två publish post/publicera inlägg, återkommer
@route("/view/publicera_inlägg.html")
def publish_post():
    return template("publicera_inlägg")

@route("/views/login.html")
def login():
    return template("login")

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
    
run(host="127.0.0.1", port=8080)