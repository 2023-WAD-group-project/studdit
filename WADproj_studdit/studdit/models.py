from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Course(models.Model):
    code = models.CharField(max_length=16, unique=True)
    title = models.CharField(max_length=32)
    upvoted_by = models.ManyToManyField(Student, related_name='course_upvotedby')
    downvoted_by = models.ManyToManyField(Student, related_name='course_downvotedby')


class Post(models.Model):
    # relational fields
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    # actual fields
    title = models.CharField(max_length=32, unique=True)
    filename = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024*10, blank=True)
    date = models.DateField(auto_now_add=True) # the auto now add param tells Django to use the date of when this entry is saved
    upvoted_by = models.ManyToManyField(Student, related_name='post_upvotedby')
    downvoted_by = models.ManyToManyField(Student, related_name='post_downvotedby')

class Comment(models.Model):
    # relational fields
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    # actual fields
    content = models.CharField(max_length=1024*10, unique=True)
    date = models.DateField(auto_now_add=True) # the auto now add param tells Django to use the date of when this entry is saved



