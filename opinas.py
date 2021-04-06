
"""
Created on Sat Mar 27 09:11:00 2021

@author: pablogtorres
"""

from flask import Flask, request, render_template
from datetime import datetime
from user_check import user_check
from forms import UserForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"
app.static_folder = 'static'

@app.route('/', methods = ['GET', 'POST'])

def landing():
    user_form = UserForm(csrf_enabled=False)
    if user_form.validate_on_submit():
        user_twitter = user_form.user.data
        results = user_check(user_twitter)
        hate_pred = results[0]
        fake_pred = results[1]
        twits = results[2]
        if hate_pred < 50.00 and fake_pred < 50.00 :
            return render_template('good.html',data=[hate_pred,fake_pred,twits])
        else:
            return render_template('bad.html', data=[hate_pred,fake_pred,twits])
    else:
        return render_template('index.html', template_form=user_form)

if __name__ == "__main__":
     # Launch the Flask dev server
     app.run(host="localhost", debug=False)
     
    