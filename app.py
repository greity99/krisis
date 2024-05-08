import os

#import modules
from flask import Flask, render_template, request, redirect, session, send_from_directory
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY") or "HEJEHEJEHEJJEEh12345"

#General functions
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
    return (check_password_uppercase(pwd) and
            check_password_lowercase(pwd) and
            check_password_digit(pwd) and
            check_password_lenght(pwd))

@app.route("/")
def index():
    """
    Returns main page. 

    Returns,
    template: index
    """
    
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
            SELECT category, city, zip_code, date, TO_CHAR(time, 'HH24:MI') AS formatted_time 
            FROM app_publish
            ORDER BY date DESC, time DESC;
            '''
        )
        
        articles = cur.fetchall()        
        conn.close()

        return render_template("index.html", articles = articles)
        
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
    return render_template("chrisis_tips.html")


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
         return render_template("publish_post.html",
                    no_category="",
                    no_zip="",
                    no_city="",
                    category="",
                    city="",
                    zip_code="")
    
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
    
    print(city)
    
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

            cur.execute(
                '''
                INSERT INTO app_publish
                VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME)
                ''', (category, city, zip_code,)
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
                    zip_code = zip_code) 

@app.route("/Kontakt")
def contact():
    """
    Returns page for contacting suupport.
    
    Returns,
    template: contact
    """
    return render_template("contact.html")

@app.route("/Logga_in", methods=['GET', 'POST'])
def login():
    '''
    Returns page for login with error message if login does not exist,
    Redirects to home page if login is correct.

    Returns,
    template: login
    '''
    
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
                    session['user_id'] = logged_in_user[0]
                    return redirect("/")
                    
                else:
                    user_name = email
                    checked_login_details = "wrong"
                    return render_template("login.html", 
                                    checked_login_details = checked_login_details, 
                                    email = email, 
                                    no_email = no_email,
                                    no_pwd = no_pwd)
            
            except psycopg2.Error as e:
                return render_template("login.html", 
                                error = "Database connection error.", 
                                checked_login_details = checked_login_details, 
                                email = email, 
                                no_email = no_email,
                                no_pwd = no_pwd)

            finally:
                if conn:
                    cur.close()
                    conn.close()
                
        return render_template("login.html", 
                    checked_login_details = checked_login_details, 
                    email = email, 
                    no_email = no_email,
                    no_pwd = no_pwd)            
        
    else:
        return render_template("login.html", 
                    checked_login_details = checked_login_details, 
                    email = email, 
                    no_email = no_email,
                    no_pwd = no_pwd)


@app.route("/Registrering")
def register():
    """
    Returns page for registering.

    Returns,
    template: register
    """
    
    return render_template("register.html", 
                    no_email_feedback="", 
                    no_birthday_feedback="", 
                    age_feedback="", 
                    no_pwd_feedback="", 
                    pwd_feedback="", 
                    email="",
                    birthday="",
                    created = False)


@app.route("/Registrering", methods=["POST"])
def register_user():
    email = request.form.get("email")
    birthday = request.form.get("birthday")
    pwd = request.form.get("pwd")

    no_email_feedback = ""
    no_birthday_feedback = ""
    age_feedback = ""
    no_pwd_feedback = ""
    pwd_feedback = ""
    
    created = False    
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
                    
                    return render_template("register.html", 
                                no_email_feedback = no_email_feedback, 
                                no_birthday_feedback = no_birthday_feedback, 
                                age_feedback = age_feedback, 
                                no_pwd_feedback = no_pwd_feedback, 
                                pwd_feedback = pwd_feedback, 
                                email = "",
                                birthday = "",
                                created = created)
                    
                except psycopg2.Error as error:
                    if conn:
                        conn.rollback()
                    return f"Error: unable to insert data\n{error}"
            else:
                pwd_feedback = "Lösenordet uppfyller inte kraven: minst en gemen, minst en versal, minst en siffra och minst 8 tecken."
                
        else:
            age_feedback = "Tyvärr uppfyller du inte ålderskraven för att registrera dig hos oss."
            return redirect("/")
        
    return render_template("register.html", 
                    no_email_feedback = no_email_feedback, 
                    no_birthday_feedback = no_birthday_feedback, 
                    age_feedback = age_feedback, 
                    no_pwd_feedback = no_pwd_feedback, 
                    pwd_feedback = pwd_feedback, 
                    email = email,
                    birthday = birthday,
                    created = created)
    

@app.route("/filter", methods=["GET"])
def filter_events():
    category = request.args.get("category") 
    city = request.args.get("city")
    zip_code = request.args.get("ZIP-code")
    date = request.args.get("date")

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
        return render_template("index.html", articles=articles)
    
    except psycopg2.Error as error:
        return f"Error: unable to retrieve data\n{error}"

@app.route("/polisen_api.html")
def polisen_api():
    return render_template("polisen_api.html")

@app.route("/static/<filename>")
def static_files(filename):
    """
    Funktion vilken returnerar statiska filer (ex. CSS) från mappen static.
    """
    return send_from_directory("static", filename)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)

