
from multiprocessing.dummy import current_process
from flask import Blueprint, render_template

from flask_security import login_required, current_user, roles_accepted

from flask_security.decorators import roles_required

from . import db

from .models import Role


main = Blueprint('main',__name__)


@main.route('/')
def principal():
    return render_template('principal.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/contacto')
def contacto():
    return render_template('contacto.html')

