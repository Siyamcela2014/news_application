from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .api_views import (
    ArticleListCreateAPIView,
    ArticleDetailAPIView,
     SubscribedArticlesAPIView,
)

urlpatterns = [
    path("token/", obtain_auth_token, name="api_token"),
    path(
        "articles/subscribed/",
         SubscribedArticlesAPIView.as_view(),
         name="subscribed_articles",
   ),
    path(
        "articles/",
        ArticleListCreateAPIView.as_view(),
        name="article_list_create",
    ),
    path(
        "articles/<int:pk>/",
        ArticleDetailAPIView.as_view(),
        name="article_detail",
    ),
]
