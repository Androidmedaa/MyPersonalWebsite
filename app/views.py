from flask import Flask, render_template, redirect, url_for, request, session, abort
from .session_interface import MySessionInterface  

app = Flask(__name__)
app.secret_key="wjfpwrf=?_23ıj'3"
app.session_interface=MySessionInterface()


def get_current_username():
    username=""
    login_auth=False
    if "username" in session:
        username=session["username"]
        login_auth=True
    return username, login_auth

@app.route('/')
def Index():
    username,login_auth=get_current_username()
    return render_template("index.html", username=username, login_auth=login_auth)
    

@app.route('/contactlist')
def ContactList():        
    username,login_auth=get_current_username()
    contactList=[
        ["Monis", "Satış",1],
        ["Josep", "Satış",1],
        ["Dilber", "Student",0],
        ["Fikri", "Data Scientist",1],
        ["Ecem", "Company",2]
    ]
    return render_template("contact_list.html", username=username, login_auth=login_auth, contactList=contactList)


@app.route('/login',methods=['GET','POST']) #login ekranımızı gösterisn diye GET kullandık
def Login():
    if request.method=='POST':
        if request.form:
            if "username" in request.form and "password" in request.form:
                username=request.form["username"]
                password=request.form["password"]
                
                if username == "admin" and password =="admin":
                    session["username"]=username
                    return redirect(url_for("Index"))
                else:
                    return redirect(url_for("Login"))
        abort(400)
    username,login_auth=get_current_username()
    return render_template("login.html",  username=username, login_auth=login_auth)



@app.route("/logout")
def Logout():
    if "username" in session:
        del session["username"]
    return redirect(url_for("Index"))

#sitemizdeki sabir kısımlar için base template kullanıcaz bunu flask teknolojisiyle yapabiliriz



# .venv\Scripts\activate bu kod ile virtual ortam aktif oluyor



