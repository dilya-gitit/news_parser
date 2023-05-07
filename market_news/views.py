from datetime import timedelta
from django.http import Http404

import finnhub
from django.utils import timezone
from rest_framework import generics, viewsets

from market_news.models import News

from .serializers import NewsSerializer


class NewsListView(generics.ListAPIView):

    serializer_class = NewsSerializer

    def get_queryset(self):
        
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        ticker = self.kwargs["ticker"]
        queryset = News.objects.filter(related=ticker)

        if date_to:
            try:
                date_to = timezone.now().strptime(date_to, "%Y-%m-%d") + timedelta(days=1)
                queryset = queryset.filter(datetime__lte=date_to)
            except ValueError:
                raise Http404('Invalid date format.')

        if date_from:
            try:
                date_from = timezone.now().strptime(date_from, "%Y-%m-%d")
                queryset = queryset.filter(datetime__gte=date_from)
            except ValueError:
                raise Http404('Invalid date format.')
               
        if not queryset.exists():
            raise Http404('No news found for the given parameters.')
        
        return queryset


class NewsViewSet(viewsets.ModelViewSet):
    def fetch_data():
        finnhub_client = finnhub.Client(
            api_key="chb2bo1r01qkns31bh20chb2bo1r01qkns31bh2g"
        )
        ticker_list = ["TSLA", "META", "AMZN", "TWTR", "NFLX"]

        today = timezone.now().date()
        yesterday = timezone.now() - timezone.timedelta(days=1)
        # Fetch existing news ids from the database
        existing_news_ids = set(
            News.objects.filter(datetime__date__range=[yesterday, today]).values_list(
                "news_id", flat=True
            )
        )

        for ticker in ticker_list:
            news_list = finnhub_client.company_news(
                ticker,
                _from={yesterday.strftime("%Y-%m-%d")},
                to={today.strftime("%Y-%m-%d")},
            )
            for news in news_list:
                news_id = news["id"]

                if news_id not in existing_news_ids:
                    News.objects.create(
                        category=news["category"],
                        datetime=timezone.now()
                        .utcfromtimestamp(news["datetime"])
                        .strftime("%Y-%m-%d %H:%M:%S"),
                        headline=news["headline"],
                        news_id=news["id"],
                        image=news["image"],
                        related=news["related"],
                        source=news["source"],
                        summary=news["summary"],
                        url=news["url"],
                    )

                    existing_news_ids.add(news_id)
