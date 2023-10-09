from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask import current_app as app
from ..models.user import User
from ..models.brandSeller import BrandSeller
from ..models.usedSeller import UsedSeller
from ..models.clothingItems import ClothingItem
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

from sqlalchemy.sql import func

@main_routes.route('/category/<int:category_id>')
def category_page(category_id):
    if category_id == 1:  # Suponiendo que 1 es el ID de "Marcas"
        # Crear la consulta base
        query = BrandSeller.query.filter_by(approved=True)

        # Filtro de búsqueda
        search_query = request.args.get('query')
        if search_query:
            query = query.filter(BrandSeller.name.contains(search_query))

        # Filtro de precio
        price_filter = request.args.get('price_filter')
        if price_filter in ["low", "medium", "high"]:
            query = query.filter(BrandSeller.price_category == price_filter)

        # Filtro de tipo de ropa
        clothing_type = request.args.get('clothing_type')
        if clothing_type in ["male", "female", "unisex"]:
            query = query.filter(BrandSeller.clothing_type == clothing_type)

        # Filtro de calificación
        rating_filter = request.args.get('rating_filter')
        if rating_filter:
            try:
                min_rating = float(rating_filter)
                query = query.filter(BrandSeller.rating >= min_rating)
            except ValueError:
                pass  # Si el valor no es un número, simplemente lo ignoramos

        # Filtro de ofertas
        on_sale = request.args.get('on_sale')
        if on_sale:
            query = query.filter(BrandSeller.on_sale == True)

        # Limite los resultados para optimizar la consulta
        brands = query.limit(50).all()  # Ajusta este número según lo que consideres apropiado

        return render_template('main_routes/brand_items.html', brands=brands)
    
    elif category_id == 2:
        # Aquí puedes replicar una lógica similar para las prendas usadas si es necesario
        return render_template('main_routes/used_items.html')

    else:
        flash("Categoría no encontrada", "danger")
        return redirect(url_for('main_routes.home'))

# Aquí es donde actualizaríamos la categoría de precio para un BrandSeller basándonos en el promedio de los precios de sus prendas
def update_brand_price_category(brand):
    avg_price = db.session.query(func.avg(ClothingItem.price)).filter(ClothingItem.brand_id == brand.id).scalar()

    # Supongamos que estos son los rangos de precio que has establecido
    if avg_price < 50:
        brand.price_category = "low"
    elif avg_price < 100:
        brand.price_category = "medium"
    else:
        brand.price_category = "high"

    db.session.commit()

# Debes llamar a update_brand_price_category(brand) cada vez que se agregue/actualice una prenda para una marca.



@main_routes.route('/brand_details/<int:brand_id>', methods=['GET'])
def brand_details(brand_id):
    # Obtén la marca específica usando brand_id
    brand = BrandSeller.query.get_or_404(brand_id)
    return render_template('main_routes/brand_details.html', brand=brand)

@main_routes.route('/prenda_details/<int:prenda_id>', methods=['GET'])
def prenda_details(prenda_id):
    # Obtén la prenda usada específica usando prenda_id
    prenda = UsedSeller.query.get_or_404(prenda_id)
    return render_template('main_routes/prenda_details.html', prenda=prenda)



#@app.route('/show_tables')
#def show_tables():
    #inspector = inspect(db.engine)
    #table_names = inspector.get_table_names()
    #return str(table_names)