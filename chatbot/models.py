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