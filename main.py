from bottle
import route, run, template, static_file, request, redirect

@route("/")
def index():
    return template("index")

@route("/views/chrisis_tips.html")
def chrisis_tips():
    return template("chrisis_tips")

@route("/view/publish_post.html")
def publish_post():
    return template("publish_post")

@route("/views/login.html")
def login():
    return template("login")
    
run(host="127.0.0.1", port=8080)