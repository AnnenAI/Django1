from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=250,unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('home')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile/', null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    website_url = models.CharField(max_length=255,null=True, blank=True)
    facebook_url = models.CharField(max_length=255,null=True, blank=True)
    twitter_url = models.CharField(max_length=255,null=True, blank=True)
    instagram_url = models.CharField(max_length=255,null=True, blank=True)


    def __str__(self):
        return str(self.user)

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    body = RichTextField()
    post_date = models.DateTimeField(default=timezone.localtime(timezone.now()))
    update_date = models.DateTimeField(default=timezone.localtime(timezone.now()))
    picture = models.ImageField(upload_to='posts/', null=True, blank=True)
    likes = models.ManyToManyField(User,related_name='blog_post')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | '+str(self.author)

    class Meta:
        ordering = ["-post_date"]

    def get_absolute_url(self):
            return reverse('show_blog',kwargs={'pk': self.author.id})

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return '%s - %s' %(self.post.title,self.name)


def check_unique_slug(sender,instance,*args,**kwards):
    slugs = dict(Post.objects.values_list('slug','id'))
    unique=False
    verifiable_slug=instance.slug
    iter=1
    while(not unique):
        if verifiable_slug in slugs and instance.id != slugs[verifiable_slug]:
            verifiable_slug=instance.slug+'-'+str(iter)
            iter+=1
        else:
            instance.slug=verifiable_slug
            unique=True

pre_save.connect(check_unique_slug,sender=Post)
