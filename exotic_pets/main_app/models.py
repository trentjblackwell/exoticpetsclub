from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    contact = models.EmailField()
    # TODO add user ID

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'post_id': self.id})




