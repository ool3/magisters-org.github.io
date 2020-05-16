from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)
# Register your models here.
admin.site.register(Category)
