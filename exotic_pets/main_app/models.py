from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    contact = models.EmailField()
    # TODO add user ID

    def __str__(self):
        return self.title




