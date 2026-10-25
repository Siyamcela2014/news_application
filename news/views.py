"""Views for displaying and managing news articles."""


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Article, Newsletter, User


def article_list(request):
    """Display approved news articles to readers."""
    articles = Article.objects.filter(approved=True).order_by(
        "-created_at"
    )
    return render(
        request,
        "news/article_list.html",
        {"articles": articles},
    )


def article_detail(request, article_id):
    """Display an approved article."""
    article = get_object_or_404(
        Article,
        id=article_id,
        approved=True,
    )
    return render(
        request,
        "news/article_detail.html",
        {"article": article},
    )


@login_required
def my_articles(request):
    """Display articles written by the logged-in user."""
    if request.user.role not in [
        User.EDITOR,
        User.JOURNALIST,
    ]:
        return HttpResponseForbidden(
            "You do not have permission to view this page."
        )

    articles = Article.objects.filter(
        author=request.user
    ).order_by("-created_at")

    return render(
        request,
        "news/my_articles.html",
        {"articles": articles},
    )


@login_required
def my_newsletters(request):
    """Display newsletters created by the logged-in user."""
    newsletters = Newsletter.objects.filter(
        author=request.user
    ).order_by("-created_at")

    return render(
        request,
        "news/my_newsletters.html",
        {"newsletters": newsletters},
    )


def vendor_dashboard(request):
    return render(request, 'news/vendor_dashboard.html')
