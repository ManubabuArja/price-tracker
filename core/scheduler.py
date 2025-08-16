from apscheduler.schedulers.background import BackgroundScheduler
from core.tracker import check_price_drops

scheduler = BackgroundScheduler()

def start_scheduler(app):
    """Start the background scheduler for price checking"""
    # Run job every 30 minutes
    scheduler.add_job(check_price_drops, 'interval', minutes=30, id="price_check", replace_existing=True)
    scheduler.start()
