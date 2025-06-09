from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import Device
from app.decorators import admin_required
from app.routes.devices import bp
from app import db

@bp.route('/inventory')
@login_required
def inventory():
    devices = Device.query.all()
    return render_template('devices/inventory.html', devices=devices)

@bp.route('/device/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_device():
    if request.method == 'POST':
        imei = request.form.get('imei')
        brand = request.form.get('brand')
        model = request.form.get('model')
        purchase_price = float(request.form.get('purchase_price'))
        
        device = Device(
            imei=imei,
            brand=brand,
            model=model,
            purchase_price=purchase_price
        )
        db.session.add(device)
        db.session.commit()
        
        flash('Device added successfully', 'success')
        return redirect(url_for('devices.inventory'))
        
    return render_template('devices/add.html')
