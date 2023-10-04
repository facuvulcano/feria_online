from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask import current_app as app
from ..models.user import User
from ..models.brandSeller import BrandSeller
from ..models.usedSeller import UsedSeller
from ..helpers import send_email
from ..extensions import bcrypt, db
from werkzeug.security import generate_password_hash, check_password_hash


main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    data = {
        'categories': [
            {'id': 1, 'name': 'Marcas'},
            {'id': 2, 'name': 'Usados'}
            # Puedes añadir más categorías aquí...
            ]
        }
    return render_template('main_routes/home.html', data=data)

@main_routes.route('/about')
def about():
    return render_template('main_routes/about.html')

@main_routes.route('/categories')
def categories():
    data = {
        'categories': [
            {'id': 1, 'name': 'Marcas'},
            {'id': 2, 'name': 'Usados'}
            # Puedes añadir más categorías aquí...
        ]
    }
    
    return render_template('main_routes/categories.html', data=data)




@main_routes.route('/brand/<brand_name>')
def brand_profile(brand_name):
    # Aquí puedes buscar información sobre la marca usando brand_name
    return render_template('main_routes/brand_profile.html')

@main_routes.route('/events')
def events():
    return render_template('main_routes/events.html')


@main_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verifica si el usuario ya existe en la base de datos
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El nombre de usuario ya existe. Prueba con otro", "danger")
            return render_template("main_routes/signup.html")
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Cuenta creada exitosamente. Por favor, inicia sesion.", "success")
        return redirect(url_for("main_routes.login"))
    
    return render_template('main_routes/signup.html')

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = username  # Puedes guardar el nombre de usuario en la sesión para acceder más tarde si lo necesitas
            return redirect(url_for('main_routes.home'))
        else:
            flash("Credenciales invalidas, por favor intentalo de nuevo", "danger")
            return redirect(url_for('main_routes.login'))

    return render_template('main_routes/login.html')


@main_routes.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main_routes.home'))

@main_routes.route('/signup_brand', methods=['GET', 'POST'])
def signup_brand():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        existing_seller = BrandSeller.query.filter_by(email=email).first()
        if existing_seller:
            flash("Este email ya está registrado. Prueba con otro", "danger")
            return render_template("main_routes/signup_brand.html")
        
        new_seller = BrandSeller(name=name, email=email)
        db.session.add(new_seller)
        db.session.commit()

        # Enviar correo notificando que su solicitud está pendiente de revisión
        send_email("Registro en Proceso", email, "Gracias por registrarte como vendedor de marca. Tu solicitud está pendiente de revisión. Te notificaremos una vez que haya sido aprobada.")
        
        flash("Registro exitoso. Gracias por registrarte como vendedor de marca. Por favor, revisa tu correo para más detalles.", "success")
        return redirect(url_for("main_routes.home"))
    
    return render_template('main_routes/signup_brand.html')

@main_routes.route('/signup_used', methods=['GET', 'POST'])
def signup_used():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        existing_seller = UsedSeller.query.filter_by(email=email).first()
        if existing_seller:
            flash("Este email ya está registrado. Prueba con otro", "danger")
            return render_template("main_routes/signup_used.html")
        
        new_seller = UsedSeller(name=name, email=email)
        db.session.add(new_seller)
        db.session.commit()

        # Enviar correo notificando que su solicitud está pendiente de revisión
        send_email("Registro en Proceso", email, "Gracias por registrarte como vendedor de usados. Tu solicitud está pendiente de revisión. Te notificaremos una vez que haya sido aprobada.")
        
        flash("Registro exitoso. Gracias por registrarte como vendedor de usados. Por favor, revisa tu correo para más detalles.", "success")
        return redirect(url_for("main_routes.home"))
    
    return render_template('main_routes/signup_used.html')



@main_routes.route('/contact')
def contact():
    return render_template('main_routes/contact.html')

@main_routes.route('/faq')
def faq():
    return render_template('main_routes/faq.html')



#@app.route('/show_tables')
#def show_tables():
    #inspector = inspect(db.engine)
    #table_names = inspector.get_table_names()
    #return str(table_names)