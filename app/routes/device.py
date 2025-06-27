import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Device, DeviceDiagnostics, db

device_bp = Blueprint('device', __name__, url_prefix='/devices')


# -------------------------------
#  Input Validation Helper
# -------------------------------
def is_valid_device_input(name, device_type, location, status):
    name_pattern = r'^[a-zA-Z0-9\s\-_.]{2,}$'
    location_pattern = r'^[a-zA-Z0-9\s\-_,.]{2,}$'
    status_values = ['online', 'offline', 'error']

    if not re.match(name_pattern, name):
        return False, "Invalid name. Use letters, numbers, space, dash, underscore, or dot."

    if not re.match(name_pattern, device_type):
        return False, "Invalid device type."

    if not re.match(location_pattern, location):
        return False, "Invalid location."

    if status.lower() not in status_values:
        return False, "Status must be: online, offline, or error."

    return True, ""


# -------------------------------
#  List Devices (with filters)
# -------------------------------
@device_bp.route('/home')
@jwt_required()
def list_devices():
    try:
        user_id = get_jwt_identity()
        search_id = request.args.get('id')
        location = request.args.get('location')
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)

        query = Device.query.filter_by(user_id=user_id)

        if search_id:
            query = query.filter(Device.id == int(search_id))
        if location:
            query = query.filter(Device.location.ilike(f'%{location}%'))
        if status:
            query = query.filter(Device.status.ilike(f'%{status}%'))

        pagination = query.paginate(page=page, per_page=5, error_out=False)

        return render_template('devices.html', devices=pagination.items, pagination=pagination, request=request)

    except Exception as e:
        current_app.logger.error("Device listing failed: %s", str(e))
        flash("Failed to load devices.", "danger")
        return redirect(url_for('main.home'))


# -------------------------------
#  Add Device
# -------------------------------
@device_bp.route('/add', methods=['GET', 'POST'])
@jwt_required()
def add_device():
    user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            name = request.form['name']
            location = request.form['location']
            device_type = request.form['device_type']
            status = request.form['status']

            valid, message = is_valid_device_input(name, device_type, location, status)
            if not valid:
                flash(message, "danger")
                return redirect(url_for('device.add_device'))

            device = Device(
                name=name,
                location=location,
                device_type=device_type,
                status=status.lower(),
                user_id=user_id
            )
            db.session.add(device)
            db.session.commit()

            flash('Device added successfully!', 'success')
            return redirect(url_for('device.list_devices'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Device creation error: %s", str(e))
            flash("Error adding device.", "danger")

    return render_template('add_device.html')


# -------------------------------
#  Update Device
# -------------------------------
@device_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def update_device(id):
    user_id = get_jwt_identity()
    device = Device.query.get_or_404(id)

    if int(device.user_id) != int(user_id):
        flash("Unauthorized access to this device.", "danger")
        return redirect(url_for('device.list_devices'))

    if request.method == 'POST':
        try:
            name = request.form['name']
            location = request.form['location']
            device_type = request.form['device_type']
            status = request.form['status']

            valid, message = is_valid_device_input(name, device_type, location, status)
            if not valid:
                flash(message, "danger")
                return redirect(url_for('device.update_device', id=id))

            device.name = name
            device.location = location
            device.device_type = device_type
            device.status = status.lower()
            db.session.commit()

            flash('Device updated successfully!', 'success')
            return redirect(url_for('device.list_devices'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Device update error (ID %s): %s", id, str(e))
            flash("Failed to update device.", "danger")

    return render_template('update_device.html', device=device)


# -------------------------------
#  Delete Device (with diagnostics)
# -------------------------------
@device_bp.route('/delete/<int:id>')
@jwt_required()
def delete_device(id):
    user_id = get_jwt_identity()
    device = Device.query.get_or_404(id)

    if int(device.user_id) != int(user_id):
        flash("Unauthorized to delete this device.", "danger")
        return redirect(url_for('device.list_devices'))

    try:
        DeviceDiagnostics.query.filter_by(device_id=device.id).delete()
        db.session.delete(device)
        db.session.commit()

        flash('Device and its diagnostics deleted successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error("Device deletion error (ID %s): %s", id, str(e))
        flash("Error deleting device.", "danger")

    return redirect(url_for('device.list_devices'))


# -------------------------------
#  Catch-All for /devices/*
# -------------------------------
@device_bp.route('/<path:subpath>')
@jwt_required()
def catch_all_device(subpath):
    flash(f"Invalid device path '/devices/{subpath}'. Redirected to Device Home.", "warning")
    return redirect(url_for('device.list_devices'))
