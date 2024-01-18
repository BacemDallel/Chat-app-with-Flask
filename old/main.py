from flask import Flask, render_template, request, session, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date, datetime
from flask import flash  # Add this import for message flashing
from sqlalchemy.exc import IntegrityError
import random
from werkzeug.utils import secure_filename
import os
import random
from string import ascii_uppercase
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qewwqewqeqw'
socketio = SocketIO(app)
bootstrap = Bootstrap5(app)

rooms = {}

def generate_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code




class JoinForm(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    room_code = StringField("Room Code:", validators=[DataRequired()])
    join = SubmitField("Join")

@app.route('/', methods=['GET', 'POST'])
def home():
    form = JoinForm()
    if form.validate_on_submit():
        # time.sleep(2)
        name = form.name.data
        room_code = form.room_code.data

        if name:
            if room_code in rooms:
                return render_template('room.html', form=form, room_code=room_code)
            else:
                flash("Room doesn't exist!", 'error')
        else:
            flash('Please provide a name!', 'error')
    else:
        return render_template('index.html', form=form)

    return render_template('index.html', form=form)

@app.route('/room/<room_code>', methods=['GET', 'POST'])
def room(room_code):
    return render_template('room.html', room_code=room_code)

@app.route('/create-room', methods=['GET', 'POST'])
def create_room():
    new_room_code = generate_code(4)  # Adjust the length as needed
    rooms[room] = {'members': 0, 'messages': []}



if __name__ == '__main__':
    socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
