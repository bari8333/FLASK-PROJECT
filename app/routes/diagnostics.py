from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import DeviceDiagnostics, Device, db

diagnostics_bp = Blueprint('diagnostics', __name__, url_prefix='/diagnostics')


# -------------------------------
#  List Diagnostics
# -------------------------------
@diagnostics_bp.route('/home')
@jwt_required()
def list_diagnostics():
    try:
        user_id = get_jwt_identity()
        sort_by = request.args.get('sort', 'timestamp')
        page = request.args.get('page', 1, type=int)
        search_id = request.args.get('id')

        if sort_by not in ['cpu_usage', 'memory_usage', 'timestamp']:
            sort_by = 'timestamp'

        user_device_ids = [d.id for d in Device.query.filter_by(user_id=user_id)]
        diagnostics_query = DeviceDiagnostics.query.filter(DeviceDiagnostics.device_id.in_(user_device_ids))

        if search_id:
            diagnostics_query = diagnostics_query.filter(DeviceDiagnostics.device_id == int(search_id))

        diagnostics_query = diagnostics_query.order_by(getattr(DeviceDiagnostics, sort_by).asc())
        pagination = diagnostics_query.paginate(page=page, per_page=5, error_out=False)

        return render_template('diagnostics.html', diagnostics=pagination.items, pagination=pagination, request=request)

    except Exception as e:
        current_app.logger.error("Error listing diagnostics: %s", str(e))
        flash("Failed to load diagnostics.", "danger")
        return redirect(url_for('main.home'))


# -------------------------------
#  Add Diagnostic
# -------------------------------
@diagnostics_bp.route('/add', methods=['GET', 'POST'])
@jwt_required()
def add_diagnostics():
    try:
        user_id = get_jwt_identity()
        devices = Device.query.filter_by(user_id=user_id).all()

        if not devices:
            flash("Please add a device before adding diagnostics.", "warning")
            return redirect(url_for('device.add_device'))

        if request.method == 'POST':
            device_id = request.form.get('device_id')
            cpu_usage = request.form.get('cpu_usage')
            memory_usage = request.form.get('memory_usage')

            device = Device.query.filter_by(id=device_id, user_id=user_id).first()
            if not device:
                flash("Invalid device selection.", "danger")
                return redirect(url_for('diagnostics.add_diagnostics'))

            diagnostic = DeviceDiagnostics(
                device_id=device.id,
                cpu_usage=cpu_usage,
                memory_usage=memory_usage
            )
            db.session.add(diagnostic)
            db.session.commit()

            flash('Diagnostic added successfully!', 'success')
            return redirect(url_for('diagnostics.list_diagnostics'))

        return render_template('add_diagnostics.html', devices=devices)

    except Exception as e:
        db.session.rollback()
        current_app.logger.error("Error adding diagnostic: %s", str(e))
        flash("Error adding diagnostic.", "danger")
        return redirect(url_for('diagnostics.add_diagnostics'))


# -------------------------------
#  Update Diagnostic
# -------------------------------
@diagnostics_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@jwt_required()
def update_diagnostics(id):
    try:
        user_id = get_jwt_identity()
        diagnostic = DeviceDiagnostics.query.get_or_404(id)

        device = Device.query.filter_by(id=diagnostic.device_id, user_id=user_id).first()
        if not device:
            user_device_ids = [d.id for d in Device.query.filter_by(user_id=user_id)]
            if diagnostic.device_id not in user_device_ids:
                flash("Unauthorized access to this diagnostic.", "danger")
                return redirect(url_for('diagnostics.list_diagnostics'))

        devices = Device.query.filter_by(user_id=user_id).all()

        if request.method == 'POST':
            new_device_id = request.form.get('device_id')
            cpu_usage = request.form.get('cpu_usage')
            memory_usage = request.form.get('memory_usage')

            new_device = Device.query.filter_by(id=new_device_id, user_id=user_id).first()
            if not new_device:
                flash("Invalid device_id selection.", "danger")
                return redirect(url_for('diagnostics.update_diagnostics', id=id))

            diagnostic.device_id = new_device.id
            diagnostic.cpu_usage = cpu_usage
            diagnostic.memory_usage = memory_usage
            db.session.commit()

            flash('Diagnostic updated successfully!', 'success')
            return redirect(url_for('diagnostics.list_diagnostics'))

        return render_template('update_diagnostics.html', diagnostic=diagnostic, devices=devices)

    except Exception as e:
        db.session.rollback()
        current_app.logger.error("Error updating diagnostic (ID %s): %s", id, str(e))
        flash("Error updating diagnostic.", "danger")
        return redirect(url_for('diagnostics.list_diagnostics'))


# -------------------------------
#  Delete Diagnostic
# -------------------------------
@diagnostics_bp.route('/delete/<int:id>')
@jwt_required()
def delete_diagnostics(id):
    try:
        user_id = get_jwt_identity()
        diagnostic = DeviceDiagnostics.query.get_or_404(id)

        device = Device.query.filter_by(id=diagnostic.device_id, user_id=user_id).first()
        if not device:
            user_device_ids = [d.id for d in Device.query.filter_by(user_id=user_id)]
            if diagnostic.device_id not in user_device_ids:
                flash("Unauthorized access to delete.", "danger")
                return redirect(url_for('diagnostics.list_diagnostics'))

        db.session.delete(diagnostic)
        db.session.commit()

        flash('Diagnostic deleted successfully!', 'success')
        return redirect(url_for('diagnostics.list_diagnostics'))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error("Error deleting diagnostic (ID %s): %s", id, str(e))
        flash("Error deleting diagnostic.", "danger")
        return redirect(url_for('diagnostics.list_diagnostics'))


# -------------------------------
#  Catch-All for /diagnostics/*
# -------------------------------
@diagnostics_bp.route('/<path:subpath>')
@jwt_required()
def catch_all_diagnostics(subpath):
    flash(f"Invalid diagnostics path '/diagnostics/{subpath}'. Redirected to Diagnostics Home.", "warning")
    return redirect(url_for('diagnostics.list_diagnostics'))
