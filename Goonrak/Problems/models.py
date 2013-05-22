from django.db import models

# Create your models here.

class Problem(models.Model):
	name = models.CharField(max_length=32)
	score = models.IntegerField()
	description = models.TextField()
