from django.urls import path

from .views import NewsListView

urlpatterns = [
    path("news/stock/<str:ticker>/", NewsListView.as_view()),
]