"""Tests for the News Application."""

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Article, User


class ArticlePermissionsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.editor = User.objects.create_user(
            username="editor_test",
            password="TestPassword123!",
            role=User.EDITOR,
        )

        self.journalist = User.objects.create_user(
            username="journalist_test",
            password="TestPassword123!",
            role=User.JOURNALIST,
        )

        self.approved_article = Article.objects.create(
            title="Approved article",
            content="This article is approved.",
            author=self.editor,
            approved=True,
        )

        self.draft_article = Article.objects.create(
            title="Journalist draft",
            content="This article is still a draft.",
            author=self.journalist,
            approved=False,
        )

    def test_journalist_can_view_approved_articles(self):
        self.client.force_authenticate(user=self.journalist)

        response = self.client.get("/api/articles/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(
                article["id"] == self.approved_article.id
                for article in response.data
            )
        )

    def test_journalist_cannot_view_drafts(self):
        self.client.force_authenticate(user=self.journalist)

        response = self.client.get("/api/articles/")

        article_ids = [article["id"] for article in response.data]

        self.assertNotIn(self.draft_article.id, article_ids)

    def test_journalist_can_create_only_drafts(self):
        self.client.force_authenticate(user=self.journalist)

        response = self.client.post(
            "/api/articles/",
            {
                "title": "New journalist draft",
                "content": "This should remain a draft.",
                "approved": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        article = Article.objects.get(
            title="New journalist draft",
            author=self.journalist,
       )

        self.assertEqual(article.author, self.journalist)
        self.assertFalse(article.approved)

    def test_journalist_cannot_update_articles(self):
        self.client.force_authenticate(user=self.journalist)

        response = self.client.patch(
            f"/api/articles/{self.approved_article.id}/",
            {"title": "Unauthorized change"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_journalist_cannot_delete_articles(self):
        self.client.force_authenticate(user=self.journalist)

        response = self.client.delete(
            f"/api/articles/{self.approved_article.id}/"
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Article.objects.filter(
                id=self.approved_article.id
            ).exists()
        )

    def test_editor_can_create_approved_articles(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.post(
            "/api/articles/",
            {
                "title": "Editor article",
                "content": "Created by an editor.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        article = Article.objects.get(title="Editor article")

        self.assertEqual(article.author, self.editor)




    def test_journalist_can_create_own_draft(self):
        self.client.force_login(self.journalist)

        response = self.client.post(
            "/api/articles/",
            {
                "title": "Journalist draft",
                "content": "This is my draft.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        article = Article.objects.filter(
          title="Journalist draft",
          author=self.journalist,
        ).latest("id")
        
        self.assertEqual(article.author, self.journalist)
        self.assertFalse(article.approved)

    def test_journalist_cannot_update_article(self):
        self.client.force_login(self.journalist)

        response = self.client.patch(
            f"/api/articles/{self.approved_article.id}/",
            {"title": "Unauthorized edit"},
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_journalist_cannot_delete_article(self):
        self.client.force_login(self.journalist)

        response = self.client.delete(
            f"/api/articles/{self.approved_article.id}/"
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Article.objects.filter(
    id=self.approved_article.id
).exists()
        )

