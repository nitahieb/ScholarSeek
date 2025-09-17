from django.urls import path
from . import views

urlpatterns = [
    path('searches/', views.SearchListCreate.as_view(), name='search-list-create'),
    path('pubmed-search/', views.PubmedSearchView.as_view(), name='pubmed-search'),
]
