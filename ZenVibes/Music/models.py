from django.db import models
from tinytag import TinyTag

class Music(models.Model):

    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('tired', 'Tired'),
        ('stressed', 'Stressed'),
        ('love', 'In Love'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    artist = models.CharField(max_length=255, blank=True, null=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    audio_file = models.FileField(upload_to='music/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # If the title or artist fields are empty and audio_file exists, read metadata using TinyTag
        if (not self.title or not self.artist) and self.audio_file:

            try:
                tag = TinyTag.get(self.audio_file.path)
                updated = False
                
                if not self.title and tag.title:
                    self.title = tag.title
                    updated = True
                
                if not self.artist and tag.artist:
                    self.artist = tag.artist
                    updated = True

                if updated:
                    self.save(update_fields = ['title', 'artist'])

            except Exception as e:
                pass


    def __str__(self):
        return f'{self.title} - {self.artist}'