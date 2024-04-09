#import modules
from bottle import run, template, route, static_file, request, redirect, error
#import psycopg2

#General variables
'''
#Databas
host = "pgserver.mau.se"
dbname = "ao7831"
user = "ao7831"
password = "diq8q181"
port = "5432"  # Default PostgreSQL port
'''


@route("/")
def index():
    """
    Returnar startsidan. 

    Returns,
    template: index
    """
    return template("index")

@route("/views/krisklar_tips.html")
def chrisis_tips():
    """
    Returns,
    template: chrisis_tips
    """
    return template("chrisis_tips")

#Denna är lite oklar, vet inte varför det finns två publish post/publicera inlägg, återkommer
@route("/view/publicera_inlägg.html")
def publish_post():
    """
    Returns,
    template: publish_post
    """
    return template("publish_post")

@route("/Kontakt")
def contact():
    """
    Returns,
    template: contact
    """
    return template("contact")

@route("/Logga in")
def login():
    """
    Returns,
    template: login
    """
    return template("login")

'''
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
'''

@route("/static/<filename>")
def static_files(filename):
    """
    Funktion vilken returnerar statiska filer (ex. CSS) från mappen static.
    """
    return static_file(filename, root="static")

run(host="127.0.0.1", port=8080)