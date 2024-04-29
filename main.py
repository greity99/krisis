import os

#import modules
from bottle import run, template, route, static_file, request, redirect, error
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("host")
dbname = os.getenv("dbname")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

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
    uppercase = False   
      
    for i in pwd:
        if i.isupper():
            uppercase = True
            break
            
        else: 
            uppercase = False
            
    if uppercase == False:
        return False
    
    else: 
        return True
        
        
def check_password_lowercase(pwd):
    '''
    Function that ensures that the password contains at least one lowercase letter.
    '''
    lowercase = False   
      
    for i in pwd:
        if i.islower():
            lowercase = True
            break
            
        else: 
            lowercase = False
            
    if lowercase == False:
        return False
    
    else: 
        return True
    
def check_password_lenght(pwd):
    '''
    Function that ensures that the password is atleast 8 characters long.
    '''
    
    length = len(pwd)
    
    if length < 8:
        return False
    
    else:
        return True
    
    
def check_password_digit(pwd):
    '''
    Function that ensures that the password contains at least one digit.
    '''
    digit = False   
      
    for i in pwd:
        if i.isdigit():
            digit = True
            break
            
        else: 
            digit = False
            
    if digit == False:
        return False
    
    else: 
        return True       
        
        
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


@route("/")
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
            SELECT category, city, zip_code, date, time FROM app_publish
            ORDER BY date DESC, time DESC;
            '''
        )
        
        articles = cur.fetchall()
        
        conn.close()

        return template("index", articles = articles)
        
    except psycopg2.Error as error:
        if conn:
            conn.rollback()
        return f"Error: unable to insert data\n{error}"
    
    



#Searchfunction index.html
#Questions:
# How to receive information about source checked by user from checkbox in HTML, is javascript needed?
# POST or GET?
# How to make a search with all fields?
'''
@route("/", method="POST")
def index():
    category = request.forms.get("category")
    city = request.forms.get("city")
    zip_code = request.forms.get("ZIP-code")
    date = request.forms.get("date")
    #Information from the two checkboxes!
    
    try:
        conn = psycopg2.connect(
            db_host = db_host,
            db_name = db_name,
            db_user = db_user,
            db_password = db_password,
            db_port = db_port
        )
        
        cur = conn.cursor()

        cur.execute(
            """
                SELECT art_title, art_text, upvote, downvote, pic
                FROM app_post
                WHERE category LIKE (%s) OR city LIKE (%s) OR zip_code LIKE (%s) OR date LIKE (%s)
            """, (category, city, zip_code, date)
        )
        
        conn.commit()

        cur.close()
        conn.close()
        

        return "Data inserted successfully!"
    
    except psycopg2.Error as error:
        if conn:
            conn.rollback()
'''

@route("/Krishantering")
def chrisis_tips():
    """
    Returns articles about how to handle different crises. 

    Returns,
    template: chrisis_tips
    """
    return template("chrisis_tips")


@route("/Ny")
def publish_post():
    """
    Returns a page on which the user can publish a post about a ongoing crisis.
    
    Returns,
    template: publish_post
    """
    return template("publish_post",
                    no_category="",
                    no_zip="",
                    no_city="",
                    category="",
                    city="",
                    zip_code="")
    
@route("/Ny", method="POST")
def publish_post():
    '''
    Form.
    Depending on the user input, the variables sent contains different content. 
    
    Returns,
    template: publish_post (if the information is not filled out correctly).
    else it redirects the user to the main page. 
    '''
    category = request.forms.get("category")
    city = request.forms.get("city")
    zip_code = request.forms.get("ZIP-code")
    
    print()
    
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

            redirect("/")  
            
        except psycopg2.Error as error:
            if conn:
                conn.rollback()
            return f"Error: unable to insert data\n{error}"
        
    return template ("publish_post",
                    no_category = no_category,
                    no_zip = no_zip,
                    no_city = no_city,
                    category = category,
                    city = city,
                    zip_code = zip_code) 

@route("/Kontakt")
def contact():
    """
    Returns page for contacting suupport.
    
    Returns,
    template: contact
    """
    return template("contact")

@route("/Logga_in")
def login():
    """
    Returns page for login.

    Returns,
    template: login
    """
    checked_login_details = ""
    email = ""
    no_email = ""
    no_pwd = ""
    
    return template("login", 
                    checked_login_details = checked_login_details, 
                    email = email, 
                    no_email = no_email,
                    no_pwd = no_pwd)


@route("/Logga_in", method=['GET', 'POST'])
def login_user():
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
    
    if request.method == 'POST':
        email = request.forms.get("email")
        pwd = request.forms.get("password")
        
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
                    redirect("/")
                    
                else:
                    user_name = email
                    checked_login_details = "wrong"
                    return template("login", 
                                    checked_login_details = checked_login_details, 
                                    email = email, 
                                    no_email = no_email,
                                    no_pwd = no_pwd)
            
            except psycopg2.Error as e:
                return template("login", 
                                error = "Database connection error.", 
                                checked_login_details = checked_login_details, 
                                email = email, 
                                no_email = no_email,
                                no_pwd = no_pwd)

            finally:
                if conn:
                    cur.close()
                    conn.close()
                
        return template("login", 
                    checked_login_details = checked_login_details, 
                    email = email, 
                    no_email = no_email,
                    no_pwd = no_pwd)            
        
    else:
        return template("login", 
                    checked_login_details = checked_login_details, 
                    email = email, 
                    no_email = no_email,
                    no_pwd = no_pwd)


@route("/Registrering")
def register():
    """
    Returns page for registering.

    Returns,
    template: register
    """
    
    return template("register.html", 
                    no_email_feedback="", 
                    no_birthday_feedback="", 
                    age_feedback="", 
                    no_pwd_feedback="", 
                    pwd_feedback="", 
                    email="",
                    birthday="")


@route("/Registrering", method="POST")
def register_user():
    email = request.forms.get("email")
    birthday = request.forms.get("birthday")
    pwd = request.forms.get("pwd")

    no_email_feedback = ""
    no_birthday_feedback = ""
    age_feedback = ""
    no_pwd_feedback = ""
    pwd_feedback = ""
    
    empty_field = "Fältet får inte lämnas tomt"
    
    # All fields empty
    if email == "" and birthday == "" and password == "":
        no_email_feedback = empty_field
        no_birthday_feedback = empty_field
        no_pwd_feedback = empty_field
    
    #email-field empty
    elif email == "" and birthday != "" and password != "":
        no_email_feedback = empty_field
    
    #birthday-field empty
    elif email != "" and birthday == "" and password != "":
        no_birthday_feedback = empty_field
    
    #password-field empty
    elif email != "" and birthday != "" and password == "":
        no_pwd_feedback = empty_field
        
    #email-field and birthday-field empty
    elif email == "" and birthday == "" and password != "":
        no_email_feedback = empty_field
        no_birthday_feedback = empty_field
    
    #email-field and password-field empty
    elif email == "" and birthday != "" and password == "":
        no_email_feedback = empty_field
        no_pwd_feedback = empty_field
    
    #birthday-field and password-field empty
    elif email != "" and birthday == "" and password == "":
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

                    redirect('/')  
                    
                except psycopg2.Error as error:
                    if conn:
                        conn.rollback()
                    return f"Error: unable to insert data\n{error}"
            else:
                pwd_feedback = "Lösenordet uppfyller inte kraven: minst en gemen, minst en versal, minst en siffra och minst 8 tecken."
                
        else:
            redirect("/")
            age_feedback = "Tyvärr uppfyller du inte ålderskraven för att registrera dig hos oss."
        
    return template("register", 
                    no_email_feedback = no_email_feedback, 
                    no_birthday_feedback = no_birthday_feedback, 
                    age_feedback = age_feedback, 
                    no_pwd_feedback = no_pwd_feedback, 
                    pwd_feedback = pwd_feedback, 
                    email = email,
                    birthday = birthday)
    

@route("/static/<filename>")
def static_files(filename):
    """
    Funktion vilken returnerar statiska filer (ex. CSS) från mappen static.
    """
    return static_file(filename, root="static")

run(host="127.0.0.1", port=8080)

