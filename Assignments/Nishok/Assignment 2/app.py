from flask import Flask, render_template, url_for, request

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=824dfd4d-99de-440d-9991-629c01b3832d.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=30119;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ccz96048;PWD=pVR3uhS6hThjZdJn",'','')


app = Flask(__name__)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register')
def new():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adduser',methods=['POST','GET'])
def adduser():
    if request.method == 'POST':
        name = request.form['name']
        rollno = request.form['rollno']
        email = request.form['email']
        password = request.form['password']

        sql = "select * from users where rollno = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,rollno)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('login.html', msg="You are already register, please log in with your credential")
        else:
            insert_sql = "insert into users values (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, rollno)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)

        return render_template('login.html',msg="You are successfully registered, please log in with your credential")

@app.route('/auth',methods=['POST','GET'])
def auth():
    if request.method == 'POST':    
        rollno = request.form['rollno']
        password = request.form['password']

        sql = "select * from users where rollno = ? and password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,rollno)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            return render_template('home.html')
        
        return render_template('login.html',msg="your roll no or password is incorrect!")



if __name__ == "__main__":
    app.run(debug=True)
