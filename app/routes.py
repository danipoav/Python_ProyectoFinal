from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from . import db, bcrypt
from .models import Usuario
from .forms import RegistroForm, LoginForm
from flask import Blueprint
from . import login_manager
from .models import Usuario

main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@main.route('/')
def home():
    return render_template('home.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistroForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            password=hashed_pw,
            rol=form.rol.data
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('✅ Cuenta creada correctamente. ¡Ya puedes iniciar sesión!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash(f'👋 Bienvenido, {usuario.nombre}', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('❌ Error en email o contraseña', 'danger')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('🔒 Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.login'))

