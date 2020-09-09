from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from datetime import datetime
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=250, blank=True)
    body = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    picture = models.ImageField(upload_to='posts/', null=True)

    def __str__(self):
        return self.title + ' | '+str(self.author)

    class Meta:
        ordering = ["-date"]

    def get_absolute_url(self):
            return reverse('show_blog')

def check_unique_slug(sender,instance,*args,**kwards):
    slugs=list(Post.objects.values_list('slug',flat=True))
    unique=False
    verifiable_slug=instance.slug
    iter=1
    while(not unique):
        if verifiable_slug in slugs:
            verifiable_slug=instance.slug+'-'+str(iter)
            iter+=1
        else:
            instance.slug=verifiable_slug
            unique=True

pre_save.connect(check_unique_slug,sender=Post)
