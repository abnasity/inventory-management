from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import Device, Sale
from app.routes.sales import bp
from app import db

@bp.route('/sales')
@login_required
def index():
    sales = Sale.query.all()
    return render_template('sales/index.html', sales=sales)

@bp.route('/sales/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        imei = request.form.get('imei')
        sale_price = float(request.form.get('sale_price'))
        payment_type = request.form.get('payment_type')
        amount_paid = float(request.form.get('amount_paid'))
        
        device = Device.query.filter_by(imei=imei, is_sold=False).first()
        if not device:
            flash('Device not found or already sold', 'danger')
            return redirect(url_for('sales.create'))
            
        sale = Sale(
            device=device,
            seller=current_user,
            sale_price=sale_price,
            payment_type=payment_type,
            amount_paid=amount_paid
        )
        
        device.is_sold = True
        db.session.add(sale)
        db.session.commit()
        
        flash('Sale recorded successfully', 'success')
        return redirect(url_for('sales.index'))
        
    return render_template('sales/create.html')

@bp.route('/sales/check_imei/<imei>')
@login_required
def check_imei(imei):
    device = Device.query.filter_by(imei=imei, is_sold=False).first()
    if device:
        return jsonify({
            'found': True,
            'brand': device.brand,
            'model': device.model,
            'purchase_price': device.purchase_price
        })
    return jsonify({'found': False})
