from flask import *
from utls import connection
from passlib.hash import sha256_crypt
import base64
#import face_recognition

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/' ,methods=['GET','POST'])
def index():
   return render_template('index.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
   if 'email' not in session:
      if request.method == "POST":
         name=request.form['name']
         email=request.form['email']
         passwd=request.form['password']
         img=request.files['image']
         img.save('static/{}.jpg'.format(email))

         encoded=sha256_crypt.encrypt(passwd)
         conn,c = connection()

         insertsql="INSERT INTO users (name ,email ,password) VALUES('{}','{}','{}');".format(name,email,encoded)
         c.execute(insertsql)
         conn.commit()
         session['email']=email
         return redirect(url_for('dashboard'))
         
      else:   
         return render_template('signup.html')
   else:
      return redirect(url_for('dashboard'))
      

@app.route('/codelogin', methods=['GET','POST'])
def login():
   if 'email' not in session:
      if request.method == "POST":
         email=request.form['email']
         passwd=request.form['password']


         conn,c = connection()

         findsql="SELECT password FROM users WHERE email='{}';".format(email)
         c.execute(findsql)
         row=c.fetchone()

         if row['password']==None:
            return('email doesnt exists')
         else:
            if sha256_crypt.verify(passwd, row['password']):
               session['email']=email
               return redirect(url_for('dashboard'))
            else:
               return ('wrong code')

      else:   
         return render_template('codelogin.html')
   else:
      return redirect(url_for('dashboard'))
   


@app.route('/logout', methods=['GET','POST'])
def logout():
   session.clear()
   if 'email' not in session:
      return redirect(url_for('index'))
   else:
      return('failed')


@app.route('/logface', methods=['GET','POST'])
def logface():
   return render_template('facelogin.html')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
   if 'email' in session:
      if True:

         conn,c = connection()

         findsql="SELECT name , email , password FROM users WHERE email='{}';".format(session['email'])
         c.execute(findsql)
         row=c.fetchone()
         return render_template('dashboard.html',row=row)



      
   else:
      return render_template('index.html')
   
      
@app.route('/upload', methods=['GET','POST'])
def upload():
   if request.method == 'POST':
      imgcode64 = request.form['file']
      with open("imagefromcamera.jpg", "wb") as fh:
         fh.write(base64.decodebytes(imgcode64))

      known_image = face_recognition.load_image_file("/content/171234_v9_bb.jpg")
      unknown_image = face_recognition.load_image_file("/content/high-jackman.jpg")

      biden_encoding = face_recognition.face_encodings(known_image)[0]
      unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
      results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
      print(results[0])         

   return render_template('signup.html')


if __name__ == '__main__':
   app.run(debug = True)




'''         if row['password']==None:
            return('email doesnt exists')
         else:
            if sha256_crypt.verify(encoded, row['password']):
               session['email']=email
               return (session['email'])
            else:
               return ('wrong code')
'''

'''

from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("password")
password2 = sha256_crypt.encrypt("password")

print(password)
print(password2)

print(sha256_crypt.verify("password", password))
		

#    if request.method == 'POST':
#        return jsonify(request.form['userID'], request.form['file'])


'''
