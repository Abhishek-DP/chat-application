from flask import Flask, render_template, url_for, session, redirect, request, jsonify, make_response
from client import Client
import time
from threading import Thread
# from database import *
# from flask_migrate import Migrate
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

NAME_KEY = "name"

client = None
messages = []
app = Flask(__name__)

app.secret_key = "hellokdggdkfgnkdfn@#NKnekdg"
# "postgresql://<username>:<password>@localhost:5432/<db_name>"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://abhi:postgrespassword!1@localhost:5432/chat_python_flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# db.init_app(app)
# migrate = Migrate(app, db)

def disconnect():
    """
    Function call before client logout
    """
    global client
    if client:
        client.disconnect()

def check_Auth(email,password):
    # chat_registration.query.filter_by(email=email, password=password).first_or_404(description='You are not registered {}'.format(email))
    pass


@app.route("/register", methods=["POST","GET"])
def register():
    """
    Register new users into the chat application
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        name = request.form["name"]
        # new_user = chat_registration(email=email,name=name,password=password)
        # db.session.add(new_user)
        # db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    """
    displays the chat window
    """
    # disconnect()
    if request.method == "POST":
        session[NAME_KEY] = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        # check_Auth(email,password)
        return redirect(url_for("home"))

    return render_template("login.html", **{"session":session})


@app.route("/logout")
def logout():
    # disconnect()
    if session:
        disconnect()
        session.pop(NAME_KEY,None)    
    return redirect(url_for("login"))

@app.route("/")
@app.route("/home")
def home():
    global client
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    # Create new session for clients
    client = Client(session[NAME_KEY])
    return render_template("index.html", **{"login": True, "session":session})

@app.route("/send_messages", methods=["POST"])
def send_messages():
    global client
    msg = request.json['messages']
    if client != None:
        client.send_messages(msg)
    update_screen = "update_screen"
    return update_screen

@app.route("/get_messages")
def get_messages():
    time.sleep(0.1)
    return jsonify({"messages":messages})

def update_messages():
    """
    updates the local list of messages
    @return: None
    """
    global messages
    while True:
        
        time.sleep(0.1) # update every 1/10th of a second
        if not client: continue
        new_messages = client.get_messages() # get any new messages from client
        messages.extend(new_messages) # add to local list of messages

        for msg in new_messages: # display new messages
            print(msg)
            if msg == "{quit}":
                break

if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True)
    