#import modules
from bottle import run, template, route
import psycopg2

#General variables
host = "pgserver.mau.se"
dbname = "ao7831"
user = "ao7831"
password = "diq8q181"
port = "5432"  # Default PostgreSQL port



@route("/")
def index():
    return template("index.html")

@route("/views/chrisis_tips.html")
def chrisis_tips():
    return template("chrisis_tips.html")

#Denna är lite oklar, vet inte varför det finns två publish post/publicera inlägg, återkommer
@route("/views/publish_post.html")
def publish_post():
    return template("publish_post.html")

@route("/views/login.html")
def login():
    return template("login.html")

#Connect to PostgreSQL
try: 
    conn = psycopg2.connect(
    host=host,
    dbname=dbname,
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