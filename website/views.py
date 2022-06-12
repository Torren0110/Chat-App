from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Messages
from . import db
from sqlalchemy.sql import func

views = Blueprint('views', __name__)
loginTime = func.now()

@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        message = request.form.get('message')

        if(len(message) > 0):
            new_message = Messages(textMessage = message, user_id = current_user.id)
            db.session.add(new_message)
            db.session.commit()

    fetchQuerry = 'SELECT messages.textmessage, messages.user_id, user.username FROM messages INNER JOIN user ON user.id = messages.user_id;'

    messages = db.session.execute(fetchQuerry)

    return render_template('home.html', user = current_user, messages = messages) 