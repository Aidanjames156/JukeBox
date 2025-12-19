from django.db import models
from django.conf import settings

class Rating(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	album_id = models.CharField(max_length=64)
	rating = models.FloatField()
	review = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = (('user', 'album_id'),)
