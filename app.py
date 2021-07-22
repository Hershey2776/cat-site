from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)

###########################################
####### The database #######################
###########################################

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///neww.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
class User1(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))




##########################################
######## The main page route ##############
###########################################


@app.route('/',methods=['GET','POST'])
def hello():
    return render_template("homepage.html")

##########################################
######## The About page route ##############
###########################################

@app.route('/about',methods=['GET','POST'])
def gallery():
    return render_template("about.html")


######################################################
################ Cats Gallery page ###################
######################################################

@app.route('/gallery',methods=['GET','POST'])
def about():
    return render_template("cats.html")




#################################################
####################################################
############ Getting a sign up form #################
########## Though it is only a gimmick################
#####################################################
################################################


@app.route('/signup', methods=["GET","POST"])
def get():
    if request.method == "GET":
        user1s = User1.query.all()
        page ='home'
        user = User1(firstname='',lastname='',email='',phone='')
        return render_template('signup.html',user1s=user1s,page=page,user=user)
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        
        newUser1 = User1(firstname=firstname,lastname=lastname,email=email)
        db.session.add(newUser1)
        db.session.commit()
        return redirect('/signup')

###########################################
########### For Deleteing a value #########
###########################################

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = User1.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/stsrh')

##########################################
######## For Editing the values ##########
##########################################

@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    user = User1.query.get_or_404(id)
    if request.method == 'POST':
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        # user.phone = request.form['phone']
        user.email = request.form['email']
        
        db.session.commit()
        return redirect('/stsrh')
    else:
        user1s = User1.query.all()
        page ='updatehome'
        return render_template('home.html',page=page,user1s=user1s,user=user)

####################################
##### Display The Edit Page########
##### Which BTW is Hidden##########
###################################


@app.route('/stsrh')
def page():
    user1s = User1.query.all()
    user = User1(firstname='',lastname='',email='',phone='')

    return render_template('home.html',user1s=user1s,page=page,user=user)

####################################################
####################################################
###### Sending The mail ############################
####################################################
####################################################



@app.route('/sendmail', methods=['GET','POST'])
def sendmail():
    l1=[]
    sent_mail=[]
    user1s = User1.query.all()
    for i in user1s:
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = 'harshsachdev45@gmail.com'
        receiver_email = i.email
        password = ("Harsh@018")
        message = """\
        Hi There

        Hi,
            We recived your details and we are glad that you showed intrest in our purrtastic cats:).
            We will get in touch with you as soon as possible."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        






    return render_template('homepage.html')



########################################################
########################################################



########################################
########### Initializing The app #######
#######################################

if __name__ == "__main__":
    app.run(debug=True)
