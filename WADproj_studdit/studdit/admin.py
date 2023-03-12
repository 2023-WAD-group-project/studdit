from django.contrib import admin
from studdit.models import Course, Student, Post, Comment

class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("title",)}

admin.site.register(Course)
admin.site.register(Post, PostAdmin)
admin.site.register(Student)
admin.site.register(Comment)

