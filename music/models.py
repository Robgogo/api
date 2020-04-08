from django.db import models

class Song(models.Model):
    # song title
    title = models.CharField(max_length=255, null=False)
    # artist names
    artist = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)
