from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    favorite_genres = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        ordering = ['user']

class TradeItem(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('traded', 'Traded'),
        ('pending', 'Pending'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='trade_items/', blank=True, null=True)
    interests = models.TextField(help_text="What you're looking for in trade")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trade_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['title']),
            models.Index(fields=['created_at']),
        ]

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username} ({self.rating} stars)"

    class Meta:
        ordering = ['-created_at']
        # Ensures a user can only review another user once.
        # If reviews are per-item, this might need adjustment or an additional constraint.
        unique_together = [['reviewer', 'reviewee']]
        indexes = [
            models.Index(fields=['reviewer', 'reviewee']),
            models.Index(fields=['reviewee', 'rating']),
        ]

    def clean(self):
        super().clean()
        if self.reviewer == self.reviewee:
            raise ValidationError("You cannot review yourself.")


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(TradeItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} wishes for {self.item.title}"

    class Meta:
        ordering = ['-added_at']
        # Ensures a user can only add an item to their wishlist once.
        unique_together = [['user', 'item']]
        indexes = [
            models.Index(fields=['user', 'item']),
        ]