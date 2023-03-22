from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Course(models.Model):
    code = models.CharField(max_length=16, primary_key=True)
    title = models.CharField(max_length=32)

    def existing_materials(self):
        return len(Post.objects.filter(course=self))

    def net_votes(self):
        return sum([x.net_votes() for x in Post.objects.filter(course=self)])

class Post(models.Model):
    # relational fields
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    
    post_author = models.ForeignKey(Student, on_delete=models.CASCADE)

    # actual fields
    title = models.CharField(max_length=32, unique=True)
    filename = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024*10, blank=True)
    date = models.DateTimeField(auto_now_add=True) # the auto now add param tells Django to use the date of when this entry is saved
    upvoted_by = models.ManyToManyField(User, related_name='post_upvotedby',blank = True)
    downvoted_by = models.ManyToManyField(User, related_name='post_downvotedby',blank = True)
    slug = models.SlugField(default="", null=False)

    def total_upvotes(self):
        return self.upvoted_by.count()
    
    def total_downvotes(self):
        return self.downvoted_by.count()

    def net_votes(self):
        return self.upvoted_by.count() - self.downvoted_by.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)



class Comment(models.Model):
    # relational fields
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # actual fields
    content = models.CharField(max_length=1024*10, unique=True)
    date = models.DateTimeField(auto_now_add=True) # the auto now add param tells Django to use the date of when this entry is saved

    upvoted_by = models.ManyToManyField(Student, related_name='comment_upvotedby', blank = True)
    downvoted_by = models.ManyToManyField(Student, related_name='comment_downvotedby', blank = True)

    def total_upvotes(self):
        return self.upvoted_by.count()
    
    def total_downvotes(self):
        return self.upvoted_by.count()


