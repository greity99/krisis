from bottle
import route, run, template, static_file, request, redirect

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
    
run(host="127.0.0.1", port=8080)