from django.db import models

class Quote(models.Model):

    text = models.TextField()
    author = models.CharField(max_length=255)
    mood = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f'{self.text[:50]}... - {self.author}'
    
    