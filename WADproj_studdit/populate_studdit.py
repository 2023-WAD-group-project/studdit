import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WADproj_studdit.settings")

import django
import studdit
django.setup()

from studdit.models import Course, Post, Student, Comment

def add_comment(post, student, content):
    comment = Comment.objects.get_or_create(post=post, conent=content)

def add_student():
    pass

def add_post(course, title, filename, description=""):
    post = Post.objects.get_or_create(course=course, title=title, filename=filename)[0]

    post.description = description

    post.save()
    return post

def add_course(code, title):
    print(code)
    print(title)
    course = Course.objects.get_or_create(code=code, title=title)[0]
    course.save()
    return course

def populate():
    courses = [
        {
            "code": "COMPSCI10001",
            "title": "CS1P",
            "posts": [{
                    "title": "anaconda install file",
                    "filename": "anaconda.exe",
                    "description": "this is the installation file for anaconda"
            }]
        },
        {
            "code": "COMPSCI2021",
            "title": "web apaplication development",
            "posts": [{
                    "title": "Rango book",
                    "filename": "rango.pdf",
                    "description": "this is the ebook for rango"
            }]
        },
        {
            "code": "COMPSCI10001",
            "title": "CS1P",
            "posts": [{
                    "title": "Phys2T scripting guide",
                    "filename": "guide.pdf",
                    "description": "this is the bash scripting guide containing good practice for bash scripting"
            }]
        },
    ]


    for course_data in courses:
        course = add_course(course_data["code"], course_data["title"])
        for post in course_data["posts"]:
            print("||||||||||||")
            print(course_data["posts"])
            print(post)
            print("||||||||||||")
            add_post(course, post["title"], post["filename"], post["description"])

if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()