from flask import Flask, render_template, request, url_for, redirect
from app import app
from flask_mysqldb import MySQL 
import MySQLdb.cursors

from random import randint

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'navi'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'search'


mysql = MySQL(app)


firstname = " "
add = 0
result = " "
age = ""
smoke = ""
alcohol = ""
measurement = ""
physical = ""
disease_family_hist = ""
patient_id = " "


# route to get data from html form and insert data into database
@app.route('/registration', methods=["GET", "POST"])
def registration():
    global patient_id
    global firstname
    middlename = " "
    lastname = " "
    email = " "
    gender = " "
    birthday = " "
    pincode = " "

    patient_id = randint(10000000000000,99999999999999)

    if request.method == "POST":
    
        firstname = request.form.get('fname')
        
        lastname = request.form['lname']
        email =  request.form['email']
        gender = request.form['gender']
        birthday = request.form['birthday']
        pincode = request.form["pincode"]
        if(firstname.isspace()):
                return render_template('registration.html',
                        error_firstname="Error: First Name can't start with a SPACE",lastname=lastname,email=email,gender=gender,
                        birthday=birthday,pincode=pincode)
               
        if(lastname.isspace()):
                return render_template('registration.html',
                        error_lastname="Error: last Name can't start with a SPACE",firstname=firstname,email=email,gender=gender,
                        birthday=birthday,pincode=pincode)               


        cursor = mysql.connection.cursor()

        cursor.execute(''' INSERT INTO patient_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(patient_id,firstname,lastname,email,gender,birthday,pincode,age,smoke,alcohol,measurement,physical,disease_family_hist,add,result))
        mysql.connection.commit()
        
   
    return render_template("ncd1.html",patientid = patient_id , fname = firstname,mname= middlename,lname =  lastname,email1 = email,gender1 = gender,birthday1 = birthday,pincode1 = pincode)




@app.route('/result1',methods=['GET',"POST"])
def result1():
    if request.method == "POST":
        count = 0

# getting the value for age

        while True :
            global age 
            global smoke 
            global alcohol 
            global measurement
            global physical 
            global disease_family_hist

        
            age = request.form['age']
            
            smoke = request.form['smoke']
            
            alcohol =request.form['alcohol']

            
            measurement = request.form['measurement']
            
            physical =  request.form['physical']



            disease_family_hist =  request.form['history']
        

            count = int(age)+int(smoke)+int(alcohol)+int(measurement)+int(physical)+int(disease_family_hist)
            
            global add 
            add = count
            print(add)
            global result
            if count>4:
                result="you need screening" 

                
 
            else:
                result="No screening needed"
 

            cursor = mysql.connection.cursor()

            query = 'UPDATE patient_info SET age  = %s,smoke = %s,alcohol = %s,measurement = %s,physical = %s,disease_family_hist = %s,count = %s,result = %s WHERE firstname = %s'
            value = (age,smoke,alcohol,measurement,physical,disease_family_hist,add,result,firstname)
            cursor.execute(query,value)
            mysql.connection.commit()
            cursor.close()

            return render_template('result1.html', add1=add,prescription=result)
    return render_template('result1.html', add1="result not found in session.")



@app.route("/searching1", methods=['GET', 'POST'])
def searching():
    if request.method == 'POST':
        x = request.form['patient if']
    
   
        
        query =  "SELECT * FROM patient_info WHERE patientid LIKE '%"+x+"%'OR firstname LIKE '%"+x+"%'OR lastname LIKE '%"+x+"%'"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        numrows = int(cursor.rowcount)
        data = cursor.fetchall()
        print(data)
        
    
        return render_template("search.html",data = data,numrows=numrows)