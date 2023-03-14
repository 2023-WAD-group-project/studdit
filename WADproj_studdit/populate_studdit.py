import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WADproj_studdit.settings")

import django
import studdit
django.setup()

from studdit.models import Course, Post, Student, Comment
from django.contrib.auth.models import User

import population_data
import shutil

def add_comment(post, student, content):
    comment = Comment.objects.get_or_create(post=post, conent=content)

def add_student():
    pass

def add_post(course, author, title, filename, description=""):
    post = Post.objects.get_or_create(course=course, post_author=author, title=title, filename=filename)[0]

    post.description = description

    post.save()
    return post

def add_course(code, title):
    print(code)
    print(title)
    course = Course.objects.get_or_create(code=code, title=title)[0]
    course.save()
    return course

def do_managepy_command(cmd):
    cmd = "manage.py " + cmd
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WADproj_studdit.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(cmd.split(" "))

def populate():
    if os.path.basename(os.getcwd()) != "WADproj_studdit":
        print(os.path.basename(os.getcwd()) + " is not the correct folder, please execute this script from inside WADproj_studdit")
        return

    try:
        shutil.rmtree(os.path.join("studdit", "migrations"))
    except FileNotFoundError:
        print("\"studdit/migrations\" folder does not exist so we did not delete it")
    try:
        shutil.rmtree("media")
    except FileNotFoundError:
        print("\"media\" folder does not exist so we did not delete it")
    try:
        os.remove("db.sqlite3")
    except FileNotFoundError:
        print("\"db.sqlite3\" file does not exist so we did not delete it")

    do_managepy_command("makemigrations studdit")
    do_managepy_command("migrate")
    User.objects.create_superuser('rooot', 'email@email.email', 'password')

    courses = population_data.courses

    authors = []

    user = User(username="Eric", email="2645295E@gla.ac.uk", password="EricPass?")
    user.save()
    user.set_password(user.password)
    user.save()
    author = Student(user=user)
    author.save()
    authors.append(author)
    user = User(username="John", email="2645295J@gla.ac.uk", password="JohnPass?")
    user.save()
    user.set_password(user.password)
    user.save()
    author = Student(user=user)
    author.save()
    authors.append(author)

    print(authors)

    for course_data in courses:

        course = add_course(course_data["code"], course_data["title"])
        for post in course_data["posts"]:
            print(post)
            print(course_data["posts"])
            add_post(course, authors[post.get("author", 0)], post["title"], post["filename"], post["description"])

    src = os.path.join("population_files", "media")
    dest = "media"
    destination = shutil.copytree(src, dest)

if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()