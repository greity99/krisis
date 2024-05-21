# Standard modules
import os
from datetime import datetime

# Imported third-party modules
from flask import Flask, render_template, request, redirect, session, send_from_directory
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Database connection details retrieved from environment variables
host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

# Flask application setup
app = Flask(__name__)

# If no secret key is found in environment variables, default key is used
app.secret_key = os.getenv("SECRET_KEY") or "HEJEHEJEHEJJEEh12345"

# General functions
def check_user_age(date_str):
    '''
    Function which takes a date as an argument and returns True if the user is 16 or older and False if the user is younger than 16.
    '''
    date = datetime.strptime(date_str, "%Y-%m-%d")
    birth_year = date.year
    year_today = date.today().year
    age = year_today - birth_year
    
    if age < 16:
        return False
    
    else:
        return True
    

#Check password
def check_password_uppercase(pwd):
    '''
    Function that ensures that the password contains at least one uppercase letter.
    '''
    return any(char.isupper() for char in pwd)
        
        
def check_password_lowercase(pwd):
    '''
    Function that ensures that the password contains at least one lowercase letter.
    '''
    return any(char.islower() for char in pwd)
    
def check_password_lenght(pwd):
    '''
    Function that ensures that the password is atleast 8 characters long.
    '''
    return len(pwd) >= 8
    

def check_password_digit(pwd):
    '''
    Function that ensures that the password contains at least one digit.
    '''
    return any(char.isdigit() for char in pwd)


def check_password_all(pwd):
    '''
    Function which includes the following functions:
    - check_password_uppercase(pwd)
    - check_password_lowercase(pwd)
    - check_password_digit(pwd)
    - check_password_lenght(pwd)
    
    and returns True if all password requirements are met. 
    '''
    uppercase = check_password_uppercase(pwd)
    lowercase = check_password_lowercase(pwd)
    digit = check_password_digit(pwd)
    length = check_password_lenght(pwd)
    
    if uppercase == True and lowercase == True and length == True and digit == True:
        return True
    
    else:
        return False
    

def is_user_logged_in():
    user_id = session.get('user_id')
    return user_id

def is_user_of_age():
    underaged = session.get('of_age')
    return underaged

def get_user_email():
    user_email = session.get('user_email')
    return user_email

def get_user_information():
    user_information = session.get('user_information')
    return user_information

def get_categories():
    try:
            conn = psycopg2.connect(
                host = host,
                dbname = dbname,
                user = user,
                password = password
            )

            cur = conn.cursor()

            cur.execute(
                '''
                SELECT category
                FROM app_category
                '''
            )
            
            categories = cur.fetchall() 
            conn.close()
            return categories
            
    except psycopg2.Error as error:
        if conn:
            conn.rollback()
            return f"Error: unable to insert data\n{error}"
    

@app.route("/")
def index():
    """
    Returns main page. 

    Returns,
    template: index
    """
    categories = get_categories()
    
    try:
        conn = psycopg2.connect(
            host = host,
            dbname = dbname,
            user = user,
            password = password
        )

        cur = conn.cursor()

        cur.execute(
            '''
            SELECT ap.category, ap.city, ap.zip_code, ap.date, TO_CHAR(ap.time, 'HH24:MI') AS formatted_time, ac.pic_text, ac.pic_url 
            FROM app_publish AS ap
            JOIN app_category AS ac
            ON ap.category = ac.category
            ORDER BY date DESC, time DESC;
            '''
        )
        
        articles = cur.fetchall()        
        conn.close()
        
        is_logged_in = is_user_logged_in()

        return render_template("index.html", 
                               articles = articles, 
                               is_logged_in = is_logged_in,
                               categories = categories)
        
    except psycopg2.Error as error:
        if conn:
            conn.rollback()
            return f"Error: unable to insert data\n{error}"

@app.route("/Krishantering")
def chrisis_tips():
    """
    Returns articles about how to handle different crises. 

    Returns,
    template: chrisis_tips
    """
    
    is_logged_in = is_user_logged_in()
    
    return render_template("chrisis_tips.html", 
                           is_logged_in = is_logged_in)


@app.route("/Ny")
def create_post():
    """
    Returns a page on which the user can publish a post about a ongoing crisis.
    
    Returns,
    template: publish_post
    """

    if not is_user_logged_in():
        return redirect("/Logga_in")
     
    else:        
        categories = get_categories()

        return render_template("publish_post.html",
                               no_category="",
                               no_zip="",
                               no_city="",
                               category="",
                               city="",
                               zip_code="",
                               categories = categories)
    

@app.route("/Ny", methods=["POST"])
def publish_post():
    '''
    Form.
    Depending on the user input, the variables sent contains different content. 
    
    Returns,
    template: publish_post (if the information is not filled out correctly).
    else it redirects the user to the main page. 
    '''

    category = request.form.get("category")
    city = request.form.get("city")
    zip_code = request.form.get("ZIP")
    
    no_category = ""
    no_zip = ""
    no_city = ""
    
    empty_field = "Fältet får inte lämnas tomt"
    
    #All fields empty
    if category == "" and city == "" and zip_code == "":
        no_category = empty_field
        no_zip = empty_field
        no_city = empty_field
    
    #category-field empty
    elif category == "" and city != "" and zip_code != "":
        no_category = empty_field
    
    #zip-field empty
    elif category != "" and city != "" and zip_code == "":
        no_zip = empty_field
        
    #city-field empty
    elif category != "" and city == "" and zip_code != "":
       no_city = empty_field
       
    #city-field and zip_code-field empty
    elif category != "" and city == "" and zip_code == "":
        no_zip=empty_field
        no_city=empty_field
    
    #city-field and category-field empty    
    elif category == "" and city == "" and zip_code != "":
        no_category = empty_field
        no_city = empty_field
        
    #zip_code-field and category-field empty    
    elif category == "" and city != "" and zip_code == "":
        no_category = empty_field
        no_zip = empty_field
        
    else:   
        try:
            conn = psycopg2.connect(
                host = host,
                dbname = dbname,
                user = user,
                password = password
            )

            cur = conn.cursor()
            is_logged_in = is_user_logged_in()

            cur.execute(
                '''
                INSERT INTO app_publish
                VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME, %s)
                ''', (category, city, zip_code, is_logged_in)
            )
            
            conn.commit()
            
            cur.close()
            conn.close()

            return redirect("/")
            
        except psycopg2.Error as error:
            if conn:
                conn.rollback()

            return f"Error: unable to insert data\n{error}"
        
    return render_template ("publish_post.html",
                    no_category = no_category,
                    no_zip = no_zip,
                    no_city = no_city,
                    category = category,
                    city = city,
                    zip_code = zip_code,
                    categories = "") 


@app.route("/Kontakt")
def contact():
    """
    Returns page for contacting suupport.
    
    Returns,
    template: contact
    """

    is_logged_in = is_user_logged_in()
    
    return render_template("contact.html",
                           is_logged_in = is_logged_in)


@app.route("/Logga_in", methods=['GET', 'POST'])
def login():
    '''
    Returns page for login with error message if login does not exist,
    Redirects to home page if login is correct.

    Returns,
    template: login
    '''

    is_logged_in = is_user_logged_in()
    
    checked_login_details = ""
    email = ""
    no_email = ""
    no_pwd = ""
    
    empty_field = "Fältet får inte lämnas tomt"
    
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")
        
        if email == "" and pwd != "":
            no_email = empty_field
            
        elif email != "" and pwd == "":
            no_pwd = empty_field
            
        elif email == "" and pwd == "":
            no_email = empty_field
            no_pwd = empty_field
                
        else:
            try:
                conn = psycopg2.connect(
                    host = host,
                    dbname = dbname,
                    user = user,
                    password = password
                )

                cur = conn.cursor()

                cur.execute(
                    '''
                    SELECT user_id 
                    FROM app_user 
                    WHERE user_mail = %s AND user_password = %s
                    ''', (email, pwd,)
                    )
                
                logged_in_user = cur.fetchone()

                if logged_in_user:
                    # Set user_id in session
                    
                    session['user_id'] = logged_in_user
                    return redirect("/")
                    
                else:
                    checked_login_details = "wrong"
                    return render_template("login.html", 
                                    checked_login_details = checked_login_details, 
                                    email = email, 
                                    no_email = no_email,
                                    no_pwd = no_pwd, 
                                    is_logged_in = is_logged_in)
            
            except psycopg2.Error as e:
                return render_template("login.html", 
                                error = "Database connection error.", 
                                checked_login_details = checked_login_details, 
                                email = email, 
                                no_email = no_email,
                                no_pwd = no_pwd, 
                                is_logged_in = is_logged_in)

            finally:
                if conn:
                    cur.close()
                    conn.close()
                
        return render_template("login.html", 
                    checked_login_details = checked_login_details, 
                    email = email, 
                    no_email = no_email,
                    no_pwd = no_pwd, 
                    is_logged_in = is_logged_in)            
        
    else:
        return render_template("login.html", 
                    checked_login_details = checked_login_details, 
                    email = email, 
                    no_email = no_email,
                    no_pwd = no_pwd, 
                    is_logged_in = is_logged_in)

@app.route("/Registrering")
def register():
    """
    Returns page for registering.

    Returns,
    template: register
    """
    underaged = is_user_of_age()
    
    return render_template("register.html", 
                    no_email_feedback="", 
                    no_birthday_feedback="", 
                    age_feedback="", 
                    no_pwd_feedback="", 
                    pwd_feedback="", 
                    email="",
                    birthday="",
                    created = False,
                    underaged = underaged)


@app.route("/Registrering", methods=["POST"])
def register_user():
    '''
    Handles user registration.

    Retrieves user information from a POST request,
    attempts to register user in PostgreSQL database table 'app_user'.
    
    Returns a template with feedback messages and form data to the client,
    message depends on success of user registration.
    '''

    email = request.form.get("email")
    birthday = request.form.get("birthday")
    pwd = request.form.get("pwd")

    no_email_feedback = ""
    no_birthday_feedback = ""
    age_feedback = ""
    no_pwd_feedback = ""
    pwd_feedback = ""
    
    created = False  
    underaged = False  
    empty_field = "Fältet får inte lämnas tomt"
    
    # All fields empty
    if email == "" and birthday == "" and pwd == "":
        no_email_feedback = empty_field
        no_birthday_feedback = empty_field
        no_pwd_feedback = empty_field
    
    #email-field empty
    elif email == "" and birthday != "" and pwd != "":
        no_email_feedback = empty_field
    
    #birthday-field empty
    elif email != "" and birthday == "" and pwd != "":
        no_birthday_feedback = empty_field
    
    #password-field empty
    elif email != "" and birthday != "" and pwd == "":
        no_pwd_feedback = empty_field
        
    #email-field and birthday-field empty
    elif email == "" and birthday == "" and pwd != "":
        no_email_feedback = empty_field
        no_birthday_feedback = empty_field
    
    #email-field and password-field empty
    elif email == "" and birthday != "" and pwd == "":
        no_email_feedback = empty_field
        no_pwd_feedback = empty_field
    
    #birthday-field and password-field empty
    elif email != "" and birthday == "" and pwd == "":
        no_birthday_feedback = empty_field
        no_pwd_feedback = empty_field
        
    else: 
        age = check_user_age(birthday)

        if age:
            checked_pwd = check_password_all(pwd)

            if checked_pwd:
                try:
                    conn = psycopg2.connect(
                        host = host,
                        dbname = dbname,
                        user = user,
                        password = password
                    )
                    
                    cur = conn.cursor()

                    cur.execute(
                        '''
                        INSERT INTO app_user (user_mail, user_password, user_birthday)
                        VALUES (%s, %s, %s)
                        ''', (email, pwd, birthday)
                    )
                    
                    conn.commit()
                    
                    cur.close()
                    conn.close()
                    
                    created = True
                    
                except psycopg2.Error as error:
                    if conn:
                        conn.rollback()

                    return f"Error: unable to insert data\n{error}"
            
            else:
                pwd_feedback = "Lösenordet uppfyller inte kraven: minst en gemen, minst en versal, minst en siffra och minst 8 tecken."
                
        else:
            underaged = True
            session['of_age'] = underaged
        
    return render_template("register.html", 
                    no_email_feedback = no_email_feedback, 
                    no_birthday_feedback = no_birthday_feedback, 
                    age_feedback = age_feedback, 
                    no_pwd_feedback = no_pwd_feedback, 
                    pwd_feedback = pwd_feedback, 
                    email = email,
                    birthday = birthday,
                    created = created,
                    underaged = underaged)
    

@app.route("/filter_kriskoll", methods=['GET'])
def filter_events():
    '''
    Retrieves and filters events based on provided parameters.

    Retrieves filtering parameters from a GET request,
    constructs a SQL query to retrieve events from 
    PostgreSQL database table 'app_publish' based on the parameters.

    Returns template "Index" as main page.
    '''
        
    category = request.args.get("category") 
    city = request.args.get("city")
    zip_code = request.args.get("ZIP-code")
    date = request.args.get("date")
    
    categories = get_categories()

    query_parts = []
    params = []

    if category:
        query_parts.append("category = %s")
        params.append(category)

    if city:
        query_parts.append("city = %s")
        params.append(city)

    if zip_code:
        query_parts.append("zip_code = %s")
        params.append(zip_code)

    if date:
        query_parts.append("date = %s")
        params.append(date)

    query_base = "SELECT category, city, zip_code, date, TO_CHAR(time, 'HH24:MI') AS formatted_time FROM app_publish"
    
    if query_parts:
        query_base += " WHERE " + " AND ".join(query_parts)

    query_base += " ORDER BY date DESC, time DESC;"

    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
        cur = conn.cursor()
        cur.execute(query_base, params)
        
        articles = cur.fetchall()
        
        cur.close()
        conn.close()
    
        is_logged_in = is_user_logged_in()
        
        return render_template("index.html", 
                               articles=articles, 
                               categories = categories,
                               is_logged_in = is_logged_in)
    
    except psycopg2.Error as error:
        return f"Error: unable to retrieve data\n{error}"


@app.route("/Händelser_från_polisen")
def polisen_api():
    is_logged_in = is_user_logged_in()
    return render_template("polisen_api.html",
                           is_logged_in = is_logged_in)

@app.route("/Profil")
def profile():
    empty_field = ""
    no_new_email = ""
    
    try:
        conn = psycopg2.connect(
            host = host,
            dbname = dbname,
            user = user,
            password = password
        )
        
        cur = conn.cursor()
        logged_in_user = is_user_logged_in()

        cur.execute(
            '''
            SELECT au.user_mail, ap.category, ap.city, ap.date
            FROM app_user AS au
            LEFT JOIN app_publish as ap
            ON au.user_id = ap.user_id
            WHERE au.user_id = %s;
            ''', (logged_in_user,)
        )
        
        user_information = cur.fetchall() 
        session['user_information'] = user_information
        
        cur.close()
        conn.close()
        
        for information in user_information:
            user_email = information[0]
            session['user_email'] = user_email
            break
        
    except psycopg2.Error as error:
        if conn:
            conn.rollback()

        return f"Error: unable to insert data\n{error}"
    
    return render_template("profile.html",
                           user_information = user_information,
                           user_email = user_email,
                           no_new_email = no_new_email,
                           empty_field = empty_field)
    
    
@app.route("/Uppdatera-email", methods = ['POST'])
def update_user_email ():
    new_email = request.form.get("Email")
    user_id = is_user_logged_in()
    user_email = get_user_email()
    user_information = get_user_information()
    
    no_new_email = ""
    empty_field = ""
    updated_email = ""
    
    if new_email != "":
        if new_email != user_email:
        
            try:
                conn = psycopg2.connect(
                    host = host,
                    dbname = dbname,
                    user = user,
                    password = password
                )
                
                cur = conn.cursor()
                cur.execute('''
                            UPDATE app_user
                            SET user_mail = %s
                            WHERE user_id = %s
                            ''', (new_email, user_id,)
                )
                
                conn.commit()
                session['user_email'] = new_email
                user_email = get_user_email()
                updated_email = "Mejladressen är nu uppdaterad!"
                
                cur.close()
                conn.close()
                
        
            except psycopg2.Error as error:
                    if conn:
                        conn.rollback()
                    return f"Error: unable to insert data\n{error}"
                
        else: 
            no_new_email = "Mejladressen du uppgav är samma som den tidigare."
    
    else: 
        empty_field = "Mejladressen uppdaterades inte. Fältet får inte lämnas tomt"
        
    return render_template("profile.html",
                           user_information = user_information,
                           user_email = user_email,
                           no_new_email = no_new_email,
                           empty_field = empty_field,
                           updated_email = updated_email)
    
        
        
        


@app.route("/index.html", methods=['POST'])
def delete_user():
    if request.method == 'POST':
        try:
            conn = psycopg2.connect(
                host = host,
                dbname = dbname,
                user = user,
                password = password
            )
            
            cur = conn.cursor()
            logged_in_user = is_user_logged_in()
            cur.execute("DELETE FROM app_publish WHERE user_id = %s", (logged_in_user,))
            cur.execute("DELETE FROM app_user WHERE user_id = %s", (logged_in_user,))
            conn.commit()
            cur.close()
            conn.close()
            
        except psycopg2.Error as error:
            if conn:
                conn.rollback()
            return f"Error: unable to insert data\n{error}"
        return redirect("/")


@app.route("/Logga_ut", methods=["GET"])
def Log_out():
    session['user_id'] = None
    return redirect("/")


@app.route("/static/<filename>")
def static_files(filename):
    """
    Funktion vilken returnerar statiska filer (ex. CSS) från mappen static.
    """
    return send_from_directory("static", filename)


# Runs the Flask app on the local machine
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8085)