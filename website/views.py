from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Messages
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        message = request.form.get('message')

        if(len(message) > 0):
            new_message = Messages(textMessage = message, user_id = current_user.id)
            db.session.add(new_message)
            db.session.commit()
            flash("done", category = "succ")
            

    return render_template('home.html', user = current_user) 