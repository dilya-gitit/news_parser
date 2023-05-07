from django.db import models


class News(models.Model):
    class Meta:
        db_table = '"market_news"'

    category = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    headline = models.CharField(max_length=500)
    news_id = models.IntegerField()
    image = models.TextField()
    related = models.CharField(max_length=50)
    source = models.CharField(max_length=100)
    summary = models.TextField()
    url = models.TextField()
