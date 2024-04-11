#import modules
from bottle import run, template, route, static_file, request, redirect, error
import psycopg2

#Databas
host = "pgserver.mau.se"
dbname = "ao7831"
user = "ao7831"
password = "diq8q181"
port = "5432"  


@route("/")
def index():
    """
    Returnar startsidan. 

    Returns,
    template: index
    """
    return template("index")

@route("/Krishantering")
def chrisis_tips():
    return template("chrisis_tips.html")



@route("/Ny")
def publish_post():
    """
    Returns,
    template: publish_post
    """
    return template("publish_post")
    
@route("/Ny", method="POST")
def publish_post():
    category = request.forms.get("category")
    city = request.forms.get("city")
    zip_code = request.forms.get("zip_code")  
    
    try:
        conn = psycopg2.connect(dbname="ao7831", user="ao7831", password="diq8q181", host="pgserver.mau.se")
        
        cursor = conn.cursor()

        sql_query = "INSERT INTO app_publish (category, city, zip_code) VALUES (%s, %s, %s)"
        publish_data = (category, city, zip_code)
 
        cursor.execute(sql_query, publish_data)
        
        conn.commit()

        cursor.close()
        conn.close()
        

        return "Data inserted successfully!"
    
    except psycopg2.Error as error:
        if conn:
            conn.rollback()
        
        return f"Error: unable to insert data\n{error}"

@route("/Kontakt")
def contact():
    """
    Returns,
    template: contact
    """
    return template("contact")

@route("/Login")
def login():
    """
    Returns,
    template: login
    """
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
    cursor = conn.cursor()
    
except psycopg2.Error as error: 
    print(f"Error: unable to connect to the database\n {error}")

@route("/static/<filename>")
def static_files(filename):
    """
    Funktion vilken returnerar statiska filer (ex. CSS) från mappen static.
    """
    return static_file(filename, root="static")

run(host="127.0.0.1", port=8080)