from django.db import models
from .utils import slugify

# Create your models here.

class Year(models.Model):
    year=models.CharField(max_length=50)
    slug=models.SlugField(unique=True,blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.year

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.year)
        super(Year, self).save(*args, **kwargs)