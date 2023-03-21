from itertools import product
from flask import Blueprint, render_template, redirect, url_for, request, flash

from werkzeug.security import generate_password_hash, check_password_hash


from flask_security import login_required, roles_accepted

from flask_security.utils import (
    login_user,
    logout_user,
    hash_password,
    encrypt_password,
)

from .models import Role, User

from . import db, userDataStore

from flask_security.decorators import roles_required

from .models import User, Product

from .forms import ProductForm
from project import forms

auth = Blueprint("auth", __name__, url_prefix="/security")


@auth.route("/login")
def login():
    return render_template("/security/login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):

        flash("El usuario y/o la contraseña son incorrectos")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for("main.profile"))


@auth.route("/register")
def register():
    return render_template("/security/register.html")


@auth.route("/register", methods=["POST"])
def register_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("El correo electrónico ya existe")
        return redirect(url_for("auth.register"))

    userDataStore.create_user(
        name=name,
        email=email,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/productos", methods=["GET"])
@login_required
@roles_required("user")
def productos():
    productos=Product.query.all() 
    return render_template("productos.html",productos=productos)


@auth.route("/administracion", methods=["GET","POST"])
@login_required
@roles_required("admin")
def administracion():
    create_form = forms.ProductForm(request.form)
    if request.method == 'POST':
        prod= Product(nombre=create_form.Nombre.data,
                        precio=create_form.Precio.data,
                        descripcion=create_form.Descripcion.data,
                        image_url=create_form.Image_url.data)
        
        db.session.add(prod)
        db.session.commit()
        
        flash('El producto se registro correctamente')
        return redirect(url_for('auth.administracion'))
    productos=Product.query.all() 
    
    return render_template("administracion.html", form=create_form,productos=productos)

@auth.route("/modificar",methods=["GET","POST"])
@login_required
@roles_required("admin")
def modificar():
    create_form2=forms.ProductForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        #Select * from alumnos where id==id
        prod1=db.session.query(Product).filter(Product.id==id).first()
        create_form2.id.data=id
        create_form2.Nombre.data=prod1.nombre
        create_form2.Precio.data=prod1.precio
        create_form2.Descripcion.data=prod1.descripcion
        create_form2.Image_url.data=prod1.image_url
        
    if request.method=='POST':
        #Select * from alumnos where id==id
        id = create_form2.id.data
        prod2=db.session.query(Product).filter(Product.id==id).first()
        
        prod2.nombre=create_form2.Nombre.data
        prod2.precio=create_form2.Precio.data
        prod2.descripcion=create_form2.Descripcion.data
        prod2.image_url=create_form2.Image_url.data
        db.session.add(prod2)
        db.session.commit()
        flash('El producto se actualizo correctamente')
        return redirect(url_for('auth.administracion'))
    return render_template('modificar.html',form=create_form2)

@auth.route("/eliminar",methods=['GET','POST'])
@login_required
@roles_required("admin")
def eliminar():
    create_form3=forms.ProductForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        #Select * from productos where id==id
        prod1=db.session.query(Product).filter(Product.id==id).first()
        create_form3.id.data=id
        create_form3.Nombre.data=prod1.nombre
        create_form3.Precio.data=prod1.precio
        create_form3.Descripcion.data=prod1.descripcion
        create_form3.Image_url.data=prod1.image_url
        
    if request.method=='POST':
        id = create_form3.id.data
        prod2=db.session.query(Product).filter(Product.id==id).first()
        prod2.nombre=create_form3.Nombre.data
        prod2.precio=create_form3.Precio.data
        prod2.descripcion=create_form3.Descripcion.data
        prod2.image_url=create_form3.Image_url.data
        db.session.delete(prod2)
        db.session.commit()
        flash('El producto se elimino correctamente')
        return redirect(url_for('auth.administracion'))
    return render_template('eliminar.html',form=create_form3)




@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.principal"))

