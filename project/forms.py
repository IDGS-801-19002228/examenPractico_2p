from email import message
from wtforms import Form
from wtforms import StringField, TelField, IntegerField, EmailField,SelectField,RadioField
from wtforms import validators
from wtforms import EmailField

from flask_wtf import FlaskForm
from  wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


def my_validate(form, field):
    if len(str(field.data)) == 0:
        raise validators.ValidationError("El campo no tiene datos")

class ProductForm(Form):
    id = IntegerField('id')
    Nombre = StringField('Nombre:')                       
    Precio = IntegerField('Precio:')
    Descripcion = StringField('Descripcion:')
    Image_url = StringField('Image_url')
    #submit = SubmitField('Enviar')
