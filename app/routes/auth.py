from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Users, Psychologists, db
from app.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = Users(username=form.username.data, email=form.email.data,
                     password_hash=hashed_password, user_type=form.user_type.data)
        db.session.add(user)
        db.session.commit()

        if form.user_type.data == 'psychologist':
            psychologist = Psychologists(user_id=user.id)
            db.session.add(psychologist)
            db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
