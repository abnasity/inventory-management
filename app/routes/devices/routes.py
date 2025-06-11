from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Device
from app.decorators import admin_required
from app.forms import DeviceForm
from app.routes.devices import bp
from app import db

@bp.route('/inventory')
@login_required
def inventory():
    devices = Device.query.all()
    device_form = DeviceForm()  # Form for the add device modal
    return render_template('devices/inventory.html', devices=devices, device_form=device_form)

@bp.route('/device/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_device():
    form = DeviceForm()
    if form.validate_on_submit():
        device = Device(
            imei=form.imei.data,
            brand=form.brand.data,
            model=form.model.data,
            purchase_price=form.purchase_price.data,
            notes=form.notes.data
        )
        db.session.add(device)
        
        try:
            db.session.commit()
            flash('Device added successfully', 'success')
            return redirect(url_for('devices.inventory'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding device: {str(e)}', 'danger')
        
    return render_template('devices/add.html', form=form)

@bp.route('/device/<imei>')
@login_required
def view_device(imei):
    """View device details"""
    device = Device.query.filter_by(imei=imei).first_or_404()
    return render_template('devices/view.html', device=device)

@bp.route('/device/<imei>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_device(imei):
    """Edit device details"""
    device = Device.query.filter_by(imei=imei).first_or_404()
    form = DeviceForm(obj=device)
    
    if form.validate_on_submit():
        form.populate_obj(device)
        
        try:
            db.session.commit()
            flash('Device updated successfully', 'success')
            return redirect(url_for('devices.inventory'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating device: {str(e)}', 'danger')
    
    return render_template('devices/edit.html', form=form, device=device)
