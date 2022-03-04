from __future__ import division, print_function
# coding=utf-8
import os,cv2,uuid,threading
import numpy as np
from gan import *
from splits import Splits
from deliver import Deliver
# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    print("index Loaded")
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        f = request.files['file-ip-1']
        email=request.form['email']
        print(email)
        user_root=f'{email}_{uuid.uuid4()}'
        print(user_root)
        os.makedirs('web',exist_ok=True)
        os.mkdir(os.path.join('web', user_root))
        file_path = os.path.join('web',user_root, secure_filename(f.filename))
        print(file_path)
        f.save(file_path)
        t=threading.Thread(target=runn,args=(file_path,email,user_root)).start()
    return render_template('submit.html')

def runn(file_path,email,user_root):
    print("runn Loaded")
    s=Splits()
    tokens,h,w,ext = s.get_tokens(file_path,user_root)
    print('Tokens created')
    print(len(tokens),w,h,ext)
    d=gan.main(user_root)
    if d:
        print('resoultions created')
        i=s.get_image('outputs/',w,ext,user_root)
        print(i,email)

        D=Deliver().send_email(email,i,user_root)

    else:
        print("Error")



if __name__ == '__main__':
    app.run(debug=False,threaded=True)