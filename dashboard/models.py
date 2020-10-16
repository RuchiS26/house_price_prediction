from django.db import models
from PIL import Image

class DataStore(models.Model):

	data = models.FileField(upload_to = "data/")
	date_added = models.DateField(auto_now_add = True)
	slug = models.SlugField(unique = True)
	name = models.CharField(max_length = 256)

	def __str__(self):
		return str(self.name)
