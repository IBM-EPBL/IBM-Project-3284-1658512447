from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_session import Session
from flask_mail import Mail, Message
import math, random, requests, json

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ccz96048;PWD=pVR3uhS6hThjZdJn",'','')


app = Flask(__name__)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ariharanariharan2001@gmail.com'
app.config['MAIL_PASSWORD'] = 'ctfoendrlrxcript'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# configuration of session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
@app.route('/home')
def home():
    if not session.get("name"):
        return redirect("/login")
    return render_template('home.html')

@app.route('/logout')
def logout():
    session["name"] = None
    return redirect("/login")

@app.route('/register',methods=['POST','GET'])
def new():    
    return render_template('register.html')

@app.route('/otp',methods=['POST','GET'])
def otp():
    username = request.form['username']
    email = request.form['email']
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 != password2:
        return render_template('register.html',msg="Password doesn't match")

    if request.method == 'POST':
        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        OTP = ""
        length = len(string)
        for i in range(6) :
            OTP += string[math.floor(random.random() * length)]
        msg = Message(
                'Greeting from Nutrition Assistant Application',
                sender = 'ariharanariharan2001@gmail.com',
                recipients = [email]
               )
        msg.body = 'OTP for registering in nutrition assistant app :  ' + OTP
        mail.send(msg)
        return render_template("verify.html",username=username,email=email,password=password1,actualotp=OTP)
    return render_template("verify.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adduser',methods=['POST','GET'])
def adduser():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        actual_otp = request.form["actualotp"]
        otp_entered = request.form['otp']

        sql = "select * from users where email = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if otp_entered != actual_otp:
            return render_template('register.html',msg="You have entered incorrect OTP")
        elif account:
            return render_template('login.html', msg="You are already register, please log in with your credential") 
        else:
            insert_sql = "insert into users values (?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)

        return render_template('login.html',msg="You are successfully registered, please log in with your credential")

@app.route('/auth',methods=['POST','GET'])
def auth():
    if request.method == 'POST':    
        password = request.form['password']
        email = request.form['email']

        sql = "select * from users where email = ? and password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            session["name"] = request.form.get("email")
            return render_template('home.html')
        
        return render_template('login.html',msg="your roll no or password is incorrect!")

@app.route('/history')
def history():
    return render_template('history.html')  

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/fetch',methods=['POST','GET'])
def fetch():
  if request.method == 'POST':
    
    description = request.form['description']

    url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"
    
    querystring = {"ingr":description}

    headers = {
	    "X-RapidAPI-Key": "2c95ef2556msh5cb6a650ce3f37ep1c3100jsn7da8f1761eee",
	    "X-RapidAPI-Host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # result = response
    result = json.loads(response.text)

    calories = 0 
    glycemicIndex = 0
    totalWeight = 0
    dietLabels = []
    healthLabels = []
    cautions = []
    totalNutrients = {}
    totalDaily = {}
    ingredients = []
    totalNutrientsKCal = {}

    if 'calories' in result:
        calories = result['calories']
    if 'glycemicIndex' in result:
        glycemicIndex = result['glycemicIndex']
    if 'totalWeight' in result:
        totalWeight = result['totalWeight']
    if 'dietLabels' in result:
        dietLabels = result['dietLabels']
    if 'healthLabels' in result:
        healthLabels = result['healthLabels']
    if 'cautions' in result:
        cautions = result['cautions']
    if 'totalNutrients' in result:
        totalNutrients = result['totalNutrients']
    if 'totalDaily' in result:
        totalDaily = result['totalDaily']
    if 'ingredients' in result:
        ingredients = result['ingredients']
    if 'totalNutrientsKCal' in result:
        totalNutrientsKCal = result['totalNutrientsKCal']
   

    # return result

    return render_template('home.html',
    calories = calories,
    glycemicIndex = glycemicIndex,
    totalWeight = totalWeight,
    dietLabels = dietLabels,
    healthLabels = healthLabels,
    cautions = cautions,
    totalNutrients = totalNutrients,
    totalDaily = totalDaily,
    ingredients = ingredients,
    totalNutrientsKCal = totalNutrientsKCal
    )

if __name__ == "__main__":
    app.run(debug=True)



