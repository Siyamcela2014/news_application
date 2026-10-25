from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """Custom user model for readers, editors, and journalists."""

    READER = "reader"
    EDITOR = "editor"
    JOURNALIST = "journalist"

    ROLE_CHOICES = [
        (READER, "Reader"),
        (EDITOR, "Editor"),
        (JOURNALIST, "Journalist"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=READER,
    )

    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        blank=True,
        related_name="subscribers",
    )
    subscribed_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="journalist_subscribers",
        limit_choices_to={"role": JOURNALIST},
    )

    def clean(self):
        """Validate fields that depend on the user's role."""
        super().clean()

        if self.role == self.JOURNALIST:
            if self.subscribed_publishers.exists():
                raise ValidationError(
                    "Journalists cannot subscribe as readers."
                )
            if self.subscribed_journalists.exists():
                raise ValidationError(
                    "Journalists cannot subscribe to other journalists."
                )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Publisher(models.Model):
    """A publishing organisation with its own editors and journalists."""

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(
        User,
        blank=True,
        related_name="edited_publishers",
        limit_choices_to={"role": User.EDITOR},
    )
    journalists = models.ManyToManyField(
        User,
        blank=True,
        related_name="publisher_affiliations",
        limit_choices_to={"role": User.JOURNALIST},
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    """A news article written independently or for a publisher."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="articles",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def clean(self):
        """Require an independent journalist or a publisher author."""
        super().clean()

        if self.publisher is None:
            if self.author.role != User.JOURNALIST:
                raise ValidationError(
                    "Independent articles must be written by journalists."
                )
        elif self.author.role not in (
            User.JOURNALIST,
            User.EDITOR,
        ):
            raise ValidationError(
                "Only journalists or editors can author publisher articles."
            )

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """A curated collection of articles."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters",
    )
    articles = models.ManyToManyField(
        Article,
        blank=True,
        related_name="newsletters",
    )

    def __str__(self):
        return self.title