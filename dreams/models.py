
from django.conf import settings
from django.db import models


class DreamSymbol(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DreamEntry(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dream_entries'
    )

    title = models.CharField(max_length=150, blank=True)
    dream_text = models.TextField()
    dream_date = models.DateField()

    symbols = models.ManyToManyField(
        DreamSymbol,
        through='DreamEntrySymbol',
        related_name='dream_entries',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-dream_date', '-created_at']

    def __str__(self):
        return self.title or f"Dream by {self.user.username} on {self.dream_date}"


class DreamEntrySymbol(models.Model):
    dream_entry = models.ForeignKey(
        DreamEntry,
        on_delete=models.CASCADE,
        related_name='symbol_tags'
    )

    dream_symbol = models.ForeignKey(
        DreamSymbol,
        on_delete=models.CASCADE,
        related_name='entry_tags'
    )

    tagged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dream_entry', 'dream_symbol'],
                name='unique_dream_symbol_tag'
            )
        ]

    def __str__(self):
        return f"{self.dream_symbol.name} - {self.dream_entry}"
