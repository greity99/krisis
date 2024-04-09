#import modules
from bottle import run, template, route
import psycopg2

# General variables
host = "pgserver.mau.se"
dbname = "ao7831"
user = "ao7831"
password = "diq8q181"
port = "5432"  # Default PostgreSQL port

# Routes
@route("/")
def index():
    return template("index.tpl")

@route("/views/krisklar_tips.html")
def chrisis_tips():
    return template("krisklar_tips.tpl")

@route("/views/publicera_inlägg.html")
def publish_post():
    return template("publicera_inlägg.tpl")

@route("/views/login.html")
def login():
    return template("login.tpl")

# Connect to PostgreSQL
try: 
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )

    # Open a cursor
    # The cursor is needed to perform database operations
    cur = conn.cursor()
    
except psycopg2.Error as error: 
    print(f"Error: unable to connect to the database\n {error}")

run(host="127.0.0.1", port=8080)
