from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from market_news.views import NewsViewSet

def run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(NewsViewSet.fetch_data, 'interval', minutes = 60)
    scheduler.start() 