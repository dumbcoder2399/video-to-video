from django.db import models

InputLang_Choices = (
    ('Arabic', 'Arabic'),
    ('Brazilian Portuguese', 'Brazilian Portuguese'),
    ('Chinese', 'Chinese'),
    ('Dutch', 'Dutch'),
    ('English-UK', 'English-UK'),
    ('English-US', 'English-US'),
    ('French', 'French'),
    ('German', 'German'),
    ('Italian', 'Italian'),
    ('Japanese', 'Japanese'),
    ('Korean', 'Korean'),
    ('Spanish', 'Spanish'),
)
OutputLang_Choices = (
    ('Arabic', 'Arabic'),
    ('Brazilian Portuguese', 'Brazilian Portuguese'),
    ('Chinese', 'Chinese'),
    ('Dutch', 'Dutch'),
    ('English-UK', 'English-UK'),
    ('English-US', 'English-US'),
    ('French', 'French'),
    ('German', 'German'),
    ('Italian', 'Italian'),
    ('Japanese', 'Japanese'),
    ('Korean', 'Korean'),
    ('Hindi', 'Hindi'),
    ('Spanish', 'Spanish'),
)

class Video(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    video = models.FileField(upload_to='Videos/')
    inputLang= models.CharField(max_length=100,choices=InputLang_Choices)
    outputLang=models.CharField(max_length=100,choices=OutputLang_Choices)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)
