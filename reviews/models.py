from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    BookName =models.CharField(max_length=200)
    author=models.CharField(max_length=100)
    writer=models.CharField(max_length=100)
    content=models.TextField()

    def __str__(self):
        return self.BookName
    

    

