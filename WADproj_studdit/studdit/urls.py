from django.urls import path
from studdit import views

urlpatterns = [
    path("home", views.home, name="home"),

    #path("course-slug-here", views.course, name="course"),
    # TODO: set up course URL mappings with slugs

    # path("post-slug-here", views.home, name="post"),
    # TODO: set up post URL mappings with slugs

    path("login", views.login, name="login"),

    path("profile", views.profile, name="profile")
]
