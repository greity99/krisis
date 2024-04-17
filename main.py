#import modules
from bottle import run, template, route, static_file, request, redirect, error
import psycopg2
from datetime import datetime

#Database
host = "pgserver.mau.se"
dbname = "ao7831"
user = "ao7831"
password = "diq8q181"
port = "5432"  


#General functions
#Testa sen med databas för att se i vilket format som datumet sparas då det skickas via formuläret
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
    return template("index")


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
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
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
    Depending on the user input, the variables sent contains different content. 
    
    Returns,
    template: publish_post (if the information is not filled out correctly).
    else it redirects the user to the main page. 
    '''
    category = request.forms.get("category")
    city = request.forms.get("city")
    zip_code = request.forms.get("ZIP-code")
    
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
    elif category !="" and city !="" and zip_code =="":
        no_zip = empty_field
        
    #city-field empty
    elif category !="" and city =="" and zip_code !="":
       no_city = empty_field
       
    #city-field and zip_code-field empty
    elif category != "" and city =="" and zip_code =="":
        no_zip=empty_field
        no_city=empty_field
    
    #city-field and category-field empty    
    elif category == "" and city =="" and zip_code !="":
        no_category = empty_field
        no_city = empty_field
        
    #zip_code-field and category-field empty    
    elif category =="" and city !="" and zip_code =="":
        category = empty_field
        no_zip = empty_field
        
    else:   
        try:
            conn = psycopg2.connect(dbname="ao7831", user="ao7831", password="diq8q181", host="pgserver.mau.se")
            cur = conn.cursor()

            cur.execute(
                '''
                INSERT INTO app_publish (category, city, zip_code, date, time)
                VALUES (%s, %s, %s, CURRENT_DATE, CURRENT_TIME)
                ''', (category, city, zip_code)
            )
            
            conn.commit()
            
            cur.close()
            conn.close()

            redirect('/')  
            
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
        
    
    
    
    
    
    
    
    '''
    #Error-handling
    #All fields empty
    if category == "" and city == "" and zip_code == "":
        return template ("publish_post",
                         no_category = empty_field,
                         no_zip = empty_field,
                         no_city = empty_field,
                         category = category,
                         city = city,
                         zip_code = zip_code)
        
    #category-field empty
    elif category == "" and city != "" and zip_code != "":
        return template ("publish_post",
                         no_category = empty_field,
                         no_zip = "",
                         no_city = "",
                         category = category,
                         city = city,
                         zip_code = zip_code)
        
    #zip-field empty
    elif category !="" and city !="" and zip_code =="":
        return template ("publish_post",
                         no_category="",
                         no_zip=empty_field,
                         no_city="",
                         category=category,
                         city=city,
                         zip_code=zip_code)
        
    #city-field empty
    elif category !="" and city =="" and zip_code !="":
        return template ("publish_post",
                         no_category="",
                         no_zip="",
                         no_city=empty_field,
                         category=category,
                         city=city,
                         zip_code=zip_code)
            
    #city-field and zip_code-field empty
    elif category != "" and city =="" and zip_code =="":
        return template ("publish_post",
                         no_category="",
                         no_zip=empty_field,
                         no_city=empty_field,
                         category=category,
                         city=city,
                         zip_code=zip_code)
    
    #city-field and category-field empty    
    elif category == "" and city =="" and zip_code !="":
        return template ("publish_post",
                         no_category=empty_field,
                         no_zip="",
                         no_city=empty_field,
                         category=category,
                         city=city,
                         zip_code=zip_code)
        
    #zip_code-field and category-field empty    
    elif category =="" and city !="" and zip_code =="":
        return template ("publish_post",
                         no_category=empty_field,
                         no_zip=empty_field,
                         no_city="",
                         category=category,
                         city=city,
                         zip_code=zip_code)
'''
      
    

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
    return template("login", checked_login_details="")


@route("/Logga in", method=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.forms.get("email")
        password = request.forms.get("password")

        try:
            conn = psycopg2.connect(dbname="ao7831", user="ao7831", password="diq8q181", host="pgserver.mau.se")
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT user_id 
                FROM app_user 
                WHERE user_mail = %s AND user_password = %s
                ''', (email, password))
            
            user = cur.fetchone()

            if user:
                redirect('/')
                
            else:
                return template("login.html", checked_login_details="wrong")
        
        except psycopg2.Error as e:
            return template('login', error="Database connection error.")

        finally:
            if conn:
                cur.close()
                conn.close()
    else:
        return template("login", checked_login_details="")



@route("/Registrering")
def register():
    """
    Returns,
    template: register
    """
    
    return template("register.html", 
                    no_email_feedback="", 
                    no_birthday_feedback="", 
                    age_feedback="", 
                    no_pwd_feedback="", 
                    pwd_feedback="", 
                    welcome_new_user="",
                    entered_email="",
                    entered_birthdate="")


@route("/Registrering", method="POST")
def register_user():
    email = request.forms.get("email")
    birthday = request.forms.get("birthday")
    password = request.forms.get("pwd")
    
    empty_field = "Detta fält får inte lämnas tomt"
    
    # All fields empty
    if email == "" and birthday == "" and password == "":
        return template("register", 
                        no_email_feedback=empty_field, 
                        no_birthday_feedback=empty_field, 
                        age_feedback="", 
                        no_pwd_feedback=empty_field, 
                        pwd_feedback="", 
                        welcome_new_user="",
                        entered_email=email,
                        entered_birthdate=birthday)
    
    else: 
        age = check_user_age(birthday)
        if age:
            pwd = check_password_all(password)
            if pwd:
                try:
                    conn = psycopg2.connect(dbname="ao7831", user="ao7831", password="diq8q181", host="pgserver.mau.se")
                    cursor = conn.cursor()

                    cursor.execute(
                        '''
                        INSERT INTO app_user (user_mail, user_password, user_birthday)
                        VALUES (%s, %s, %s)
                        ''', (email, password, birthday)
                    )
                    
                    conn.commit()
                    cursor.close()
                    conn.close()

                    redirect('/')  
                    
                except psycopg2.Error as error:
                    if conn:
                        conn.rollback()
                    return f"Error: unable to insert data\n{error}"
            else:
                pwd_feedback = "Lösenordet uppfyller inte kraven: minst en gemen, minst en versal, minst en siffra och minst 8 tecken."
                return template("register", 
                                no_email_feedback="", 
                                no_birthday_feedback="", 
                                age_feedback="", 
                                no_pwd_feedback="",  
                                pwd_feedback=pwd_feedback, 
                                welcome_new_user="",
                                entered_email=email,
                                entered_birthdate=birthday)
        else:
            age_feedback = "Tyvärr uppfyller du inte ålderskraven för att registrera dig hos oss."
            return template("register", 
                            no_email_feedback="", 
                            no_birthday_feedback="", 
                            age_feedback=age_feedback, 
                            no_pwd_feedback="", 
                            pwd_feedback="", 
                            welcome_new_user="",
                            entered_email="",
                            entered_birthdate="")

@route("/static/<filename>")
def static_files(filename):
    """
    Funktion vilken returnerar statiska filer (ex. CSS) från mappen static.
    """
    return static_file(filename, root="static")

run(host="127.0.0.1", port=8080)

