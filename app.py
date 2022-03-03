from __future__ import division, print_function
# coding=utf-8
import pip
pip.main(['install', 'basicsr==1.3.4.9'])
pip.main(['install', 'facexlib==0.2.2'])
pip.main(['install', 'gfpgan==1.3.2'])
import os,cv2,uuid,threading
from PIL import Image
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
    # for i in os.listdir('inputs'):
    #     os.remove(os.path.join('inputs', i))
    # for i in os.listdir('results'):
    #     os.remove(os.path.join('results', i))
    # for i in os.listdir('outputs'):
    #     os.remove(os.path.join('outputs', i))
    # for i in os.listdir('web'):
    #     os.remove(os.path.join('web', i))
    # print('Paths cleared')
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
        basepath = os.path.dirname(__file__)
        os.mkdir(os.path.join(basepath, 'web', user_root))
        file_path = os.path.join(basepath, 'web',user_root, secure_filename(f.filename))
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