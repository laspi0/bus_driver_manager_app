from flask import Flask, redirect, render_template, request, url_for
from model import Contact, db, User

from flask import request

from flask import request
from datetime import date
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:laspi@localhost:5432/contact"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    contact = Contact.query.get_or_404(id)
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    contact.name = name
    contact.last_name = last_name
    contact.email = email
    contact.phone = phone
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET'])
def show_update_form(id):
    contact = Contact.query.get_or_404(id)
    return render_template('update.html', contact=contact)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect('/')

@app.route("/", methods=['GET', 'POST'])
def index():
    contacts = Contact.query.order_by(Contact.created_at).all()
    return render_template('index.html', contacts=contacts)


@app.route('/add_contact', methods=['GET'])
def add_contact_form():
    return render_template('add_contact.html')

# Route pour enregistrer un contact
@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    # Assurez-vous d'avoir l'ID de l'utilisateur approprié pour assigner le contact
    user_id = 1  # Remplacez cette valeur par la logique appropriée pour récupérer l'ID de l'utilisateur

    # Création d'une instance du modèle Contact
    contact = Contact(name=name, last_name=last_name, phone=phone, email=email, user_id=user_id)

    # Ajout du contact à la base de données
    db.session.add(contact)
    db.session.commit()

    return redirect('/')




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5008)
