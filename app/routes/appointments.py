import json
from datetime import datetime, timezone

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db  # Import db from app/__init__.py

from app.models import Psychologists, Appointments  # Import models from app/__init__.py

bp = Blueprint('appointments', __name__, url_prefix='/appointments')


@bp.route('/make_appointment/<int:id>', methods=['POST'])
@login_required
def make_appointment(id):
    psychologist = Psychologists.query.get(id)
    if psychologist:
        selected_time = request.form.get('selected_time')
        if selected_time:
            appointment_day, appointment_hour = selected_time.split(':')
            appointment_hour = int(appointment_hour)
            working_hours = json.loads(psychologist.working_hours)
            if (
                appointment_day in working_hours
                and str(appointment_hour) in working_hours[appointment_day]
                and working_hours[appointment_day][str(appointment_hour)] == 'Available'
            ):
                working_hours[appointment_day][str(appointment_hour)] = 'Unavailable'
                psychologist.working_hours = json.dumps(working_hours)
                db.session.commit()

                appointment = Appointments(
                    user_id=current_user.id,
                    psychologist_id=id,
                    appointment_time={appointment_day: {str(appointment_hour): 'Booked'}},
                    created_at=datetime.now(timezone.utc)
                )
                db.session.add(appointment)
                db.session.commit()
                flash('Appointment booked successfully!', 'success')
            else:
                flash('Selected time slot is not available for booking!', 'error')
        else:
            flash('No time selected for appointment!', 'error')
    else:
        flash('Psychologist not found!', 'error')

    return redirect(url_for('main.index'))

@bp.route('/cancel_appointment/<int:id>', methods=['POST'])
@login_required
def cancel_appointment(id):
    appointment = Appointments.query.get(id)
    if appointment and appointment.user_id == current_user.id:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment canceled successfully!', 'success')
        return redirect(url_for('users.profile'))
    else:
        flash('Appointment not found or unauthorized!', 'error')
        return redirect(url_for('users.profile'))
