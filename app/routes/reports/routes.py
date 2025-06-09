from flask import render_template, jsonify, request
from flask_login import login_required
from app.decorators import admin_required
from app.models import Sale, Device
from app.routes.reports import bp
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get time ranges for comparison
    today = datetime.now()
    thirty_days_ago = today - timedelta(days=30)
    previous_thirty_days = thirty_days_ago - timedelta(days=30)
    
    # Current period stats
    current_sales = Sale.query.filter(Sale.created_at >= thirty_days_ago).count()
    current_revenue = db.session.query(
        func.sum(Sale.sale_price)
    ).filter(Sale.created_at >= thirty_days_ago).scalar() or 0
    
    # Previous period stats for growth calculation
    previous_sales = Sale.query.filter(
        Sale.created_at >= previous_thirty_days,
        Sale.created_at < thirty_days_ago
    ).count()
    previous_revenue = db.session.query(
        func.sum(Sale.sale_price)
    ).filter(
        Sale.created_at >= previous_thirty_days,
        Sale.created_at < thirty_days_ago
    ).scalar() or 0
    
    # Calculate growth percentages
    sales_growth = ((current_sales - previous_sales) / previous_sales * 100) if previous_sales > 0 else 0
    revenue_growth = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
    
    # Get basic stats
    stats = {
        'total_sales': current_sales,
        'total_revenue': current_revenue,
        'sales_growth': round(sales_growth, 1),
        'revenue_growth': round(revenue_growth, 1),
        'available_devices': Device.query.filter_by(is_sold=False).count(),
        'outstanding_credit': db.session.query(
            func.sum(Sale.sale_price - Sale.amount_paid)
        ).filter(Sale.is_fully_paid == False).scalar() or 0
    }
    
    # Get sales data for chart
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sales_data = db.session.query(
        func.date(Sale.created_at).label('date'),
        func.count(Sale.id).label('count')
    ).filter(
        Sale.created_at >= thirty_days_ago
    ).group_by(
        func.date(Sale.created_at)
    ).all()
    
    chart_data = {
        'dates': [str(row.date) for row in sales_data],
        'sales': [row.count for row in sales_data]
    }
    
    # Get payment type breakdown
    payment_data = {
        'cash_sales': Sale.query.filter_by(payment_type='cash').count(),
        'credit_sales': Sale.query.filter_by(payment_type='credit').count()
    }
    
    # Get recent sales
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(5).all()
    
    # Get top products
    top_products = db.session.query(
        Device.brand,
        Device.model,
        func.count(Sale.id).label('total_sold'),
        func.sum(Sale.sale_price).label('revenue')
    ).join(Sale).group_by(
        Device.brand,
        Device.model
    ).order_by(
        func.count(Sale.id).desc()
    ).limit(5).all()
    
    return render_template('reports/dashboard.html',
                         stats=stats,
                         chart_data=chart_data,
                         payment_data=payment_data,
                         recent_sales=recent_sales,
                         top_products=top_products)

@bp.route('/reports/summary')
@login_required
@admin_required
def summary():
    days = request.args.get('days', 30, type=int)
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Get sales metrics
    total_sales = Sale.query.filter(Sale.created_at >= cutoff_date).count()
    total_revenue = db.session.query(
        func.sum(Sale.sale_price)
    ).filter(
        Sale.created_at >= cutoff_date
    ).scalar() or 0
    
    # Calculate growth rates
    prev_cutoff = cutoff_date - timedelta(days=days)
    prev_sales = Sale.query.filter(
        Sale.created_at.between(prev_cutoff, cutoff_date)
    ).count()
    prev_revenue = db.session.query(
        func.sum(Sale.sale_price)
    ).filter(
        Sale.created_at.between(prev_cutoff, cutoff_date)
    ).scalar() or 0
    
    sales_growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0
    revenue_growth = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0
    
    return jsonify({
        'sales_metrics': {
            'total_sales': total_sales,
            'sales_growth': round(sales_growth, 1),
            'total_revenue': round(total_revenue, 2),
            'revenue_growth': round(revenue_growth, 1)
        },
        'inventory_metrics': {
            'available_devices': Device.query.filter_by(is_sold=False).count()
        },
        'credit_metrics': {
            'total_outstanding': db.session.query(
                func.sum(Sale.sale_price - Sale.amount_paid)
            ).scalar() or 0
        }
    })
