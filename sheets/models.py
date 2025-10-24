from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """A high-level category for entries, e.g., 'Django ORM' or 'Nmap'."""
    title = models.CharField(max_length=200, unique=True)
    #  add a user link later for multi-user support
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Entry(models.Model):
    """A specific cheatsheet entry with a title and content."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=255)
    summary = models.TextField(
        blank=True, 
        help_text="Quick summary or key points for the front of the flashcard. Markdown is supported."
    )
    content = models.TextField(help_text="Detailed explanation for the back of the flashcard. Markdown is supported.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-created_at'] # Show newest entries first

    def __str__(self):
        return self.title