from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, User, Newsletter, Publisher
from .serializers import (
    ArticleSerializer,
    UserSerializer,
    NewsletterSerializer,
    PublisherSerializer,
)


class IsJournalist(permissions.BasePermission):
    """Allow access only to journalists."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.JOURNALIST
        )


class IsEditor(permissions.BasePermission):
    """Allow access only to editors."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.EDITOR
        )



class ArticleListCreateAPIView(generics.ListCreateAPIView):
    """List approved articles and allow article creation."""

    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == User.EDITOR:
            return Article.objects.all().order_by("-created_at")

        if user.role == User.JOURNALIST:
            return Article.objects.filter(
                approved=True
            ).order_by("-created_at")

        return Article.objects.filter(
            approved=True
        ).order_by("-created_at")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]

        return [permissions.IsAuthenticatedOrReadOnly()]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == User.EDITOR:
            serializer.save(author=user)
        elif user.role == User.JOURNALIST:
            serializer.save(author=user, approved=False)
        else:
            raise PermissionDenied(
                "Only editors and journalists can create articles."
            )


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an article."""

    
    def get_queryset(self):
        user = self.request.user

        if user.role == User.EDITOR:
            return Article.objects.all()

        if user.is_authenticated:
            return Article.objects.filter(
                author=user
            ) | Article.objects.filter(approved=True)

        return Article.objects.filter(approved=True)

    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]


    
    def update(self, request, *args, **kwargs):
        article = self.get_object()

        if request.user.role == User.JOURNALIST:
            if article.author != request.user:
                raise PermissionDenied(
                    "You can only update your own articles."
                )
        elif request.user.role != User.EDITOR:
            raise PermissionDenied(
                "Only editors and the article's journalist can update."
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        article = self.get_object()

        if request.user.role == User.JOURNALIST:
            if article.author != request.user:
                raise PermissionDenied(
                    "You can only delete your own articles."
                )
        elif request.user.role != User.EDITOR:
            raise PermissionDenied(
                "Only editors and the article's journalist can delete."
            )

        return super().destroy(request, *args, **kwargs)


class SubscribedArticlesAPIView(generics.ListAPIView):
    """List approved articles from subscribed publishers and journalists."""

    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role != User.READER:
            raise PermissionDenied(
                "Only readers can view subscribed articles."
            )

        publisher_articles = Article.objects.filter(
            approved=True,
            publisher__in=user.subscribed_publishers.all(),
        )

        journalist_articles = Article.objects.filter(
            approved=True,
            author__in=user.subscribed_journalists.all(),
        )

        return (
            publisher_articles | journalist_articles
        ).distinct().order_by("-created_at")
