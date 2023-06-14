from operator import or_
from flask import Flask, redirect, render_template, request, session
from flask_login import current_user
from decorators import login_required
from model import Contact, db, User
from functools import wraps
from sqlalchemy import or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:laspi@localhost:5432/contact"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'laspi'

db.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def route_login():
    return login()
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            # Ajoutez d'autres informations de l'utilisateur à la session selon vos besoins
            return redirect('/')
        else:
            return redirect('/login')
    else:
        return render_template('login.html')



@app.route('/update/<int:id>', methods=['POST'])
@login_required
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
@login_required
def show_update_form(id):
    contact = Contact.query.get_or_404(id)
    return render_template('update.html', contact=contact)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect('/')



@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    search_query = request.args.get('search')

    # Récupérer les contacts filtrés en fonction de la recherche
    if search_query:
        contacts = Contact.query.filter(
            Contact.user_id == session['user_id'],
            or_(
                Contact.name.ilike(f"%{search_query}%"),
                Contact.last_name.ilike(f"%{search_query}%")
            )
        ).order_by(Contact.created_at).all()
    else:
        contacts = Contact.query.filter_by(user_id=session['user_id']).order_by(Contact.created_at).all()

    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['GET'])
@login_required
def add_contact_form():
    return render_template('add_contact.html')


@app.route('/add_contact', methods=['POST'])
@login_required
def add_contact():
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    # Assurez-vous d'avoir l'ID de l'utilisateur approprié pour assigner le contact
    user_id = 2  # Remplacez cette valeur par la logique appropriée pour récupérer l'ID de l'utilisateur

    # Création d'une instance du modèle Contact
    contact = Contact(name=name, last_name=last_name, phone=phone, email=email, user_id=user_id)

    # Ajout du contact à la base de données
    db.session.add(contact)
    db.session.commit()

    return redirect('/')


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Vérifiez si l'utilisateur existe déjà dans la base de données
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists')

        # Créez un nouvel utilisateur
        new_user = User(username=username, password=password)

        # Ajoutez le nouvel utilisateur à la base de données
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')
    else:
        return render_template('register.html')

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect('/login')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5008)
