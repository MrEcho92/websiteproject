from django.db import models
from django.utils import timezone
# Create your models here.
STATUS = ((0,'Draft'), (1, 'Publish'))

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image_upload = models.ImageField(upload_to='image', max_length=100)



    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
