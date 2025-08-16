import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from markupsafe import escape

from core.tracker import track_once, list_products, get_history, ensure_alert
from core.comparator import compare_urls

main = Blueprint("main", __name__)


@main.route("/")
def index():
    products = list_products()
    return render_template("index.html", products=products)


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