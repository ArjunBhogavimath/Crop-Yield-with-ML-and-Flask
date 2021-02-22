from flask import Flask,redirect,render_template,request,flash,url_for
import sqlite3
import pickle

crop=Flask(__name__)


@crop.route('/')

def home():
    
    return render_template('index.html')

@crop.route('/register.html')

def register():
    return render_template('register.html')      


@crop.route('/register', methods=['POST'])
def registration():
    error = None;
    
    
    if request.method=="POST":
        
        name=request.form['name']
        mail=request.form['mail']
        uname=request.form['uname']
        passw=request.form['passw']
        repassw=request.form['repassw']
        if passw==repassw:            
            with sqlite3.connect('cropdb.db') as con:
                a=con.cursor()
                a.execute('insert into register(fname,email,uname,password) values(?,?,?,?)',(name,mail,uname,passw,))
                con.commit()
                return  render_template('login.html')
        else :
            error = "password should be same"
            return  render_template('register.html',error=error)
        

@crop.route('/login.html')
def login():
    
    return render_template('login.html')

	
@crop.route('/login',methods=['POST'])

def savelog():
    error=None;
    if request.method=="POST":
        uname=request.form['uname']
        passw=request.form['passw']
        con=sqlite3.connect('cropdb.db')
        a=con.cursor()
        a.execute("select * from register where uname=?",(uname,))
        b=a.fetchone()
       

        username=b[3]
        password=b[4]
        if uname == username and passw == password:
            flash("You are successfully logged in")
            return  render_template('crop.html')
            
        else:
            error="Invalid username or password"
            return  render_template('login.html',error=error)   

@crop.route('/crop.html')
def cropl():
    
    return render_template('crop.html')


@crop.route('/crop',methods=['POST'])

def cropdetails():
    if request.method=="POST":
        a="crop.pickle"
        model=pickle.load(open(a,"rb"))
        cr={'January':0,'February':1,'March':2,'April':3,'May':4,'June':5,'July':6,'August':7,'September':8,'October':9,'November':10,'December':11,
            'Rice':0,'Sugarcane':1,'Ragi':2,'Cotton':3,'Corn':4,'Wheat':5,'Millet':6,
            'Yes':0,'No':1,'Coimbatore':0,'Dindigul':1,'Madurai':2,'Salem':3,'Theni':4,'Trichy':5,
            'Sandy_soil':0,'Clayey_soil':1,'Loamy_soil':2}
        a=request.form['month']
        a=cr[a]
        b=float(request.form['time'])
        c=int(request.form['min'])
        d=int(request.form['max'])
        e=float(request.form['rain'])
        f=float(request.form['humidity'])
        g=request.form['Select_Crops']
        g=cr[g]
        h=request.form['Irrigation']
        h=cr[h]
        i=request.form['Your_District']
        i=cr[i]
        j=request.form['Soil_Type']
        j=cr[j]
        k=float(request.form['Area'])
        s=model.predict([[a,b,c,d,e,f,g,h,i,j,k]])
        if s[0]==1:
            return render_template("result.html")
        else:
            return  render_template('crop.html')
            
    
    return render_template('crop.html')



@crop.route('/result')
def result():
    
    return render_template('result.html')


if __name__=='__main__':
    crop.secret_key='abc'
    crop.run(debug=True)
