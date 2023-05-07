from flask import make_response,Flask, flash, redirect, render_template, request, url_for, session
from app import *
import bcrypt

@app.route('/')
def home():
    return render_template('index.html')

#Login
@app.route('/login', methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        user = db.user.find_one({'email':session['email']})
        type = user['type']
        if type == 'user':
            return redirect('/user')
        else:
            return redirect('/dashboard')

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        type = request.form.get("type")
        email_found = db.user.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            user_type = email_found['type']
            if type == user_type:
                if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                    session["email"] = email_val
                    if type == 'user':
                        return redirect('/user')
                    else:
                        return redirect('/dashboard')
                else:
                    if "email" in session:
                        return redirect(url_for("logged_in"))
                    message = 'Wrong password'
                    return render_template('login.html', message=message)
            else:
                message = "Type invalid"
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)

    return render_template('login.html', message=message)

#SignUp
@app.route('/register', methods=["POST", "GET"])
def signup():
    message = ''
    if "email" in session:
        return redirect('/dashboard')

    if request.method == "POST":
        user = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password")
        password2 = request.form.get("cpassword")
        phno = request.form.get("phno")
        type = request.form.get("type")

        email_found = db.user.find_one({"email": email})
        
        if email_found:
            message = 'This email already exists in database'
            return render_template('login.html', message=message)
        
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)

        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed, 'phoneNo':phno, 'type':type}
            db.user.insert_one(user_input)
            
            user_data = db.user.find_one({"email": email})
            new_email = user_data['email']
   
            return redirect('/dashboard')

    return render_template('register.html')

#logout
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect('/login')
    else:
        return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if "email" in session:
        user = db.user.find({'email':session['email']})   
        return render_template('dashboard.html')
    else:
        return redirect('/login')

@app.route('/user')    
def user():
    if "email" in session:
        user = db.user.find({'email':session['email']})   
        return render_template('user.html')
    else:
        return redirect('/login') 