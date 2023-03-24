from django.urls import path
from studdit import views
from studdit.views import LikePostView

from studdit.API import get_courses, get_posts


urlpatterns = [
    path("home", views.home, name="home"),

    path("", views.home, name="index"),

    path('course/<slug:course_name_slug>/', views.show_course, name='show_course'),

    path("course/<slug:course_name_slug>/post/<slug:slug>", views.post, name="post"),

    path('course/<slug:course_name_slug>/post/<slug:post_slug>/comment', views.add_comment, name='comment'),

    path('course/<slug:course_code>/post/<slug:post_slug>/delete_post/', views.delete_post, name='delete_post'),

    path('course/<slug:course_name_slug>/add_post/', views.add_post, name='add_post'),

    path("login", views.login_page, name="login"),

    path("profile", views.profile, name="profile"),

    path("profile/delete_account", views.delete_account, name="delete_account"),

    path('like_post/', views.LikePostView.as_view(), name='like_post'),

    path("test", views.test, name="test"),

    path('dislike_post/', views.DislikePostView.as_view(), name='dislike_post'),

    # API endpoints
    path("get_courses", get_courses, name="API_get_courses"),

    path("get_posts", get_posts, name="API_get_posts"),

    # form submission links
    path("user_login", views.user_login, name="user_login"),

    path("register", views.register, name="register"),

    path("logout", views.log_out, name="logout"),

    path("change_username", views.change_username, name="change_username"),

    path("change_password", views.change_password, name="change_password"),

]
