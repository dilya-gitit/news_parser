from django.apps import AppConfig

class MarketNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market_news'
    
    def ready(self) -> None:
        from .jobs import scheduler
        scheduler.run()