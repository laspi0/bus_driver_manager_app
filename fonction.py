import datetime
from flask import jsonify, render_template, request
from app import app, db
from model import Contact, User

def add_user(username, email, password):
    with app.app_context():
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

add_user('admin', 'john@exame.com', 'passer')


def add_contact(name, phone, user_id):
    contact = Contact(name=name, phone=phone, user_id=user_id, created_at=datetime.utcnow())
    db.session.add(contact)
    db.session.commit()
    return contact

