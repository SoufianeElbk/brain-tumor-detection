import tensorflow as tf 
import numpy as np 
import cv2
from flask import Flask, request, render_template, redirect, session

app = Flask(__name__)
app.secret_key = 'flask'

path_to_model = 'model.h5'
my_model = tf.keras.models.load_model(path_to_model)

def model_predict(img_path, my_model):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))
    img = np.expand_dims(img, axis=0)
    result = my_model.predict(img)
    if result > 0.3:
        return 'This is a Tumor'
    else:
        return 'This is not a Tumor'


@app.route('/index',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        imgfile = request.files['img']
        img_path = "./static/images/"+imgfile.filename
        imgfile.save(img_path)
        res = model_predict(img_path, my_model)
        return render_template('index.html',predection=res,imp=img_path)
    return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    if username =='admin' and password =='admin' :
      session['username'] = username
      return redirect('/index')
    else:
      return render_template('login.html', error='Invalid username or password')
  else:
    return render_template('login.html')


@app.route('/index',methods=['GET','POST'])
def index():
  if 'username' in session:
    return render_template('index.html')
  else:
    return redirect('/login')


@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
