from django.contrib import admin
from blogapp.models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'filename', 'date')
admin.site.register(Post, PostAdmin)