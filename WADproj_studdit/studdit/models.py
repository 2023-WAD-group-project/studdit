from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=16, unique=True)
    title = models.CharField(max_length=32)

class Post(models.Model):
    # relational fields
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # actual fields
    title = models.CharField(max_length=32, unique=True)
    filename = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024*10, blank=True)
    date = models.DateField(auto_now_add=True) # the auto now add param tells Django to use the date of when this entry is saved

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Comment(models.Model):
    # relational fields
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    # actual fields
    content = models.CharField(max_length=1024*10, unique=True)
    date = models.DateField(auto_now_add=True) # the auto now add param tells Django to use the date of when this entry is saved


# note these are just intermediary models to store upvote data,
# since there is no easy & reasonable way to do this via a field in existing models.
# also note that with the current setup it's possible to upvote the same thing twice,
# the workaround being that we should use get or create when handling an upvote request
# which should hopefully ensure no duplicates occur.
class PostVote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=True)
class CommentVote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=True)
