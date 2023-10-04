from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import current_app as app
from ..models.user import User
from ..models.brandSeller import BrandSeller
from ..models.usedSeller import UsedSeller
from ..helpers import send_email
from ..extensions import db

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/admin/pending_sellers', methods=['GET'])
def pending_sellers():
    # Vendedores no aprobados
    brand_sellers = BrandSeller.query.filter_by(approved=False).all()
    used_sellers = UsedSeller.query.filter_by(approved=False).all()
    
    # Vendedores aprobados
    brand_sellers_approved = BrandSeller.query.filter_by(approved=True).all()
    used_sellers_approved = UsedSeller.query.filter_by(approved=True).all()

    return render_template('admin/pending_sellers.html', 
                           brand_sellers=brand_sellers, 
                           used_sellers=used_sellers,
                           brand_sellers_approved=brand_sellers_approved,
                           used_sellers_approved=used_sellers_approved)



@admin_routes.route('/admin/approve_brand_seller/<int:seller_id>', methods=['GET'])
def approve_brand_seller(seller_id):
    seller = BrandSeller.query.get(seller_id)
    if seller:
        seller.approved = True
        db.session.commit()
        # Enviar correo notificando aprobación
        send_email("Aprobación de Registro", seller.email, "¡Felicitaciones! Tu registro como vendedor de marca ha sido aprobado. Ahora puedes acceder y comenzar a vender.")
        flash("Vendedor de marca aprobado con éxito.", "success")
    else:
        flash("Vendedor no encontrado.", "danger")

    return redirect(url_for('admin_routes.pending_sellers'))


@admin_routes.route('/admin/approve_used_seller/<int:seller_id>', methods=['GET'])
def approve_used_seller(seller_id):
    seller = UsedSeller.query.get(seller_id)
    if seller:
        seller.approved = True
        db.session.commit()
        # Enviar correo notificando aprobación
        send_email("Aprobación de Registro", seller.email, "¡Felicitaciones! Tu registro como vendedor de usados ha sido aprobado. Ahora puedes acceder y comenzar a vender.")
        flash("Vendedor de usados aprobado con éxito.", "success")
    else:
        flash("Vendedor no encontrado.", "danger")

    return redirect(url_for('admin_routes.pending_sellers'))


@admin_routes.route('/admin/delete_brand_seller/<int:seller_id>', methods=['GET'])
def delete_brand_seller(seller_id):
    seller_to_delete = BrandSeller.query.get(seller_id)
    if seller_to_delete:
        db.session.delete(seller_to_delete)
        db.session.commit()
        flash("Vendedor de marca eliminado con éxito.", "success")
    else:
        flash("Vendedor de marca no encontrado.", "danger")
    return redirect(url_for('admin_routes.pending_sellers'))

@admin_routes.route('/admin/delete_used_seller/<int:seller_id>', methods=['GET'])
def delete_used_seller(seller_id):
    seller_to_delete = UsedSeller.query.get(seller_id)
    if seller_to_delete:
        db.session.delete(seller_to_delete)
        db.session.commit()
        flash("Vendedor de usados eliminado con éxito.", "success")
    else:
        flash("Vendedor de usados no encontrado.", "danger")
    return redirect(url_for('admin_routes.pending_sellers'))


@admin_routes.route('/admin/users', methods=['GET'])
def view_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_routes.route('/admin/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for('admin_routes.view_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash("Usuario eliminado con éxito", "success")
    
    return redirect(url_for('admin_routes.view_users'))