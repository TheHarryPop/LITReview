from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following',
                             null=True, blank=True)
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='followed_by', null=True, blank=True)

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
