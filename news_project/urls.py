from django.contrib import admin
from django.urls import path
from news import views
from django.urls import include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.article_list, name="article_list"),
    path(
        "article/<int:article_id>/",
        views.article_detail,
        name="article_detail",
    ),
    path("my-articles/", views.my_articles, name="my_articles"),
    path(
        "my-newsletters/",
        views.my_newsletters,
        name="my_newsletters",
    ),    
        path("vendor-dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
        path("api/", include("news.api_urls")),
]
