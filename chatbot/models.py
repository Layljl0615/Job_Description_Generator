from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Past(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=250)
    answer = models.TextField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-created_at']


# Extended user profile with security question
class UserProfile(models.Model):
    SECURITY_QUESTIONS = [
        ('color', 'What is your favorite color?'),
        ('food', 'What is your favorite food?'),
        ('city', 'What city were you born in?'),
        ('pet', 'What was the name of your first pet?'),
        ('teacher', 'What was the name of your favorite teacher?'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question = models.CharField(max_length=10, choices=SECURITY_QUESTIONS)
    security_answer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Profile"
