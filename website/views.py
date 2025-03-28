from flask import Blueprint, render_template, request,redirect,url_for
from flask_socketio import emit
from . import socketio, connected_users
from .models import User, Location
from . import db
from flask_login import login_user, login_required, logout_user, current_user


views = Blueprint('views', __name__)



@views.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    return render_template('home.html')

@socketio.on('location')
def handle_location(data):
    if not current_user.is_authenticated:
        return
    
    new_location = Location(
        longitude= data['lon'],
        latitude= data['lat'],
        user_id = current_user.id
    )
    db.session.add(new_location)
    db.session.commit()
    
    connected_users[current_user.id] = {
        'lat' : data['lat'],
        'lon' :data['lon'],
        'username': current_user.username
    }
    emit('update', connected_users[current_user.id], broadcast=True)
    

