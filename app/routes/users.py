from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash

from app.forms import EditProfileForm, WorkingHoursForm, DummyForm
from app.models import Users, Chats, Articles, Psychologists, Appointments
from app import db
import json

bp = Blueprint('users', __name__)


@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = Users.query.get(current_user.id)
    psychologist = Psychologists.query.filter_by(user_id=current_user.id).first()

    psychologists = Psychologists.query.all()
    users = Users.query.all()

    working_hours = psychologist.working_hours if psychologist else {}

    appointments = Appointments.query.all()

    # for normal users
    appointment_psychologist = None
    for appointment in appointments:
        for find_appointment_psychologist in psychologists:
            if appointment.psychologist_id == find_appointment_psychologist.id and current_user.id == appointment.user_id:
                appointment_psychologist = find_appointment_psychologist

    # for psychologists
    # Create a dictionary to map user IDs to users
    user_dict = {user.id: user for user in users}

    for appointment in appointments:
        # Check if the user ID associated with the appointment exists in the user dictionary
        if appointment.user_id in user_dict:
            appointment_user = user_dict[appointment.user_id]
        else:
            appointment_user = None

    if isinstance(working_hours, str):
        working_hours = json.loads(working_hours)

    # Fetch all articles if the user is an admin
    articles = Articles.query.all() if user.user_type == 'admin' else current_user.articles

    return render_template('users/profile.html', user=user, working_hours=working_hours,
                           articles=articles, appointments=appointments,
                           appointment_psychologist=appointment_psychologist,
                           appointment_user=appointment_user, form=WorkingHoursForm())


@bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data

        if current_user.user_type == 'psychologist':
            psychologist = current_user.psychologist
            psychologist.name = form.name.data
            psychologist.age = form.age.data
            psychologist.specialization = form.specialization.data

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('users.profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address

        if current_user.user_type == 'psychologist' and current_user.psychologist:
            form.name.data = current_user.psychologist.name or "No information provided yet!!!"
            form.age.data = current_user.psychologist.age or "No information provided yet!!!"
            form.specialization.data = current_user.psychologist.specialization or "No information provided yet!!!"

    return render_template('users/edit_profile.html', form=form)


@bp.route('/profile/delete', methods=['POST'])
@login_required
def delete_profile():
    user = current_user
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/profile/update_working_hours', methods=['POST'])
@login_required
def update_working_hours():
    psychologist = Psychologists.query.filter_by(user_id=current_user.id).first()
    if not psychologist:
        flash("Psychologist details not found. Please contact support.", 'error')
        return redirect(url_for('users.profile'))

    working_hours = request.form.get('working_hours')
    try:
        working_hours = json.loads(working_hours)
    except json.JSONDecodeError:
        flash('Invalid data format for working hours.', 'error')
        return redirect(url_for('users.profile'))

    psychologist.working_hours = json.dumps(working_hours)
    db.session.commit()
    flash('Working hours updated successfully!', 'success')
    return redirect(url_for('users.profile'))
