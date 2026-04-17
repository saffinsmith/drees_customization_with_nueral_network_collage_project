# Create your models here.
from django.db import models


class PartsImage(models.Model):
    shirt_parts_image_id = models.AutoField(primary_key=True)
    shirt_parts_id = models.CharField(max_length=100)
    file_path = models.ImageField(upload_to='parts_image/')
    component_name = models.CharField(max_length=200)

    class Meta:
        db_table = "shirt_parts_images"
