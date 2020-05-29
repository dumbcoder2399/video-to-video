from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='Videos/')
    inputLang= models.CharField(max_length=100)
    outputLang=models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)
