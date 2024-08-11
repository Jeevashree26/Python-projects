from flask import Flask ,render_template, request, redirect, url_for, session
import mysql.connector as MySQLdb
import re


app = Flask(__name__)
app.secret_key = '\xa2yaS\x91*\x17\xe8\x8a?\xdc\xe2x\xc7\xb2\xf9\x82\xe0\xec\tj\x94\xf6\x05'


try:

    conn = MySQLdb.connect(
        host ='127.0.0.1',
        user = 'root',
        password = 'Root@123',
        database = 'students_app'

    )

    mycur = conn.cursor()
    print('database connected')
except:
    print('database connection error')




@app.route('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mycur.execute("select * from login_acc where username = %s and password = %s",(username, password))
        acc = mycur.fetchone()
        if acc:
            session['loggedin'] = True
            session['id'] = acc[0]
            session['username'] = acc[1]
            msg = "Logged in successfully!!"
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html',msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mycur.execute("select * from login_acc where username = %s",(username,))
        acc = mycur.fetchone()

        if acc:
            msg = 'Account already exists!!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'INvalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Name must contain only character and numbers !!!'
        else:
            mycur.execute("INSERT INTO login_acc VALUES (NULL, %s, %s, %s)", (username, password, email))
            conn.commit()
            msg = "You have successfully registered !!!"

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)

@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))

@app.route("/display")
def display():
    if 'loggedin' in session:
        mycur.execute("select * from login_acc where id = %s",(session['id'],))
        acc = mycur.fetchone()
        return render_template('display.html', account=acc)
    return redirect(url_for('login'))

@app.route("/update", methods=['GET', 'POST'])
def update():
    msg =""
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            ssql = mycur.execute("select * from login_acc where username = %s", (username,))
            update_acc = mycur.fetchone()
            if update_acc:
                msg = "Account already exists !!!"
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'INvalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Name must contain only character and numbers !!!'
            else:
                mycur.execute("update login_acc set username = %s, password = %s, email = %s where id = %s",(username, password, email, (session['id'])))
                conn.commit()
                msg = "you have successfully updated !!"
        elif request.method == 'POST':
            msg = "Please fill out the form !!"
        return render_template('update.html', msg=msg)
    return redirect(url_for('login'))   

@app.route("/delete")
def delete():
    if 'loggedin' in session:
        mycur.execute("delete from login_acc where id = %s",(session['id'],))
        conn.commit()
        return render_template('delete.html')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)