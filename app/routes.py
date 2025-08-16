import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from markupsafe import escape

from core.tracker import track_once, list_products, get_history, ensure_alert
from core.comparator import compare_urls, search_products_by_name

main = Blueprint("main", __name__)


@main.route("/")
def index():
    products = list_products()
    return render_template("index.html", products=products)


@main.route("/search", methods=["GET", "POST"])
def search():
    """Search for products by name across multiple websites"""
    search_results = []
    search_query = ""
    recommendations = []
    
    if request.method == "POST":
        search_query = request.form.get("product_name", "").strip()
        if search_query:
            try:
                # Search for products across multiple websites
                search_results = search_products_by_name(search_query)
                
                # Generate recommendations based on price and rating
                if search_results:
                    recommendations = generate_recommendations(search_results)
                    
            except Exception as e:
                flash(f"Search failed: {escape(str(e))}", "danger")
    
    return render_template("search.html", 
                         search_results=search_results, 
                         search_query=search_query,
                         recommendations=recommendations)


@main.route("/track", methods=["POST"])
def track():
    url = request.form.get("url", "").strip()
    target_price = request.form.get("target", "").strip() or request.form.get("target_price", "").strip()

    if not url:
        flash("Please provide a URL.", "danger")
        return redirect(url_for("main.index"))

    try:
        target = float(target_price) if target_price else None
    except ValueError:
        flash("Target price must be a number.", "danger")
        return redirect(url_for("main.index"))

    try:
        product_id, res = track_once(url)
        if target is not None:
            ensure_alert(product_id, email=None, target_price=target)  # email can be set later
        flash(f"Tracked: {res.title} @ ₹{res.price:.2f}", "success")
        return redirect(url_for('main.history_item', product_id=product_id))
    except Exception as e:
        flash(f"Failed to track URL: {escape(str(e))}", "danger")
        return redirect(url_for("main.index"))


@main.route("/history")
def history():
    products = list_products()
    return render_template("history.html", products=products, history=None)


@main.route("/history/<int:product_id>")
def history_item(product_id: int):
    products = list_products()
    history = get_history(product_id)
    return render_template("history.html", products=products, history=history, selected=product_id)


@main.route("/compare", methods=["GET", "POST"])
def compare():
    results = []
    pasted = ""
    if request.method == "POST":
        pasted = request.form.get("urls", "").strip()
        urls = [u.strip() for u in pasted.splitlines() if u.strip()]
        if urls:
            results = compare_urls(urls)
    return render_template("compare.html", results=results, pasted=pasted)


def generate_recommendations(search_results):
    """Generate recommendations based on price and rating"""
    if not search_results:
        return []
    
    # Filter out results without price or rating
    valid_results = [r for r in search_results if r.get('price') and r.get('rating')]
    
    if not valid_results:
        return []
    
    # Sort by price (ascending) and rating (descending)
    sorted_results = sorted(valid_results, key=lambda x: (x['price'], -x['rating']))
    
    recommendations = []
    
    # Best price recommendation
    best_price = min(valid_results, key=lambda x: x['price'])
    recommendations.append({
        'type': 'best_price',
        'title': '💰 Best Price',
        'message': f"Lowest price at {best_price['platform']}",
        'product': best_price
    })
    
    # Best value recommendation (price/rating ratio)
    best_value = min(valid_results, key=lambda x: x['price'] / max(x['rating'], 1))
    if best_value != best_price:
        recommendations.append({
            'type': 'best_value',
            'title': '⭐ Best Value',
            'message': f"Best price-to-rating ratio at {best_value['platform']}",
            'product': best_value
        })
    
    # Highest rating recommendation
    best_rating = max(valid_results, key=lambda x: x['rating'])
    if best_rating != best_price and best_rating != best_value:
        recommendations.append({
            'type': 'best_rating',
            'title': '🏆 Highest Rating',
            'message': f"Highest rating at {best_rating['platform']}",
            'product': best_rating
        })
    
    return recommendations