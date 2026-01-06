from django.db import models
from django.conf import settings


class Notification(models.Model):
	"""Simple in-app notifications"""
	TYPE_CHOICES = [
		('exchange_proposed', 'Exchange Proposed'),
		('exchange_accepted', 'Exchange Accepted'),
		('message', 'Message'),
	]

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='notifications'
	)
	type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='message')
	message = models.CharField(max_length=255)
	url = models.CharField(max_length=255, blank=True)
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'notifications'
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['user', 'is_read']),
		]

	def __str__(self):
		return f"Notification for {self.user.username}: {self.message[:30]}"
