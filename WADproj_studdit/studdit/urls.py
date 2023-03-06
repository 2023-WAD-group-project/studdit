from django.urls import path
from studdit import views

urlpatterns = [
    path("home", views.home, name="home"),

    path("course", views.course, name="course"),
    # TODO: set up course URL mappings with slugs
    
    path('course/<slug:course_name_slug>/', views.show_course,name='show_course'),

    path("post", views.post, name="post"),

    path("login", views.login, name="login"),

    path("profile", views.profile, name="profile"),

    path('course/<slug:course_name_slug>/add_post/', views.add_post, name='add_post'),
]
