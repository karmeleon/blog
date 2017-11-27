from django.contrib import admin
from blogapp.models import Post, Image

# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'filename', 'date')

class ImageAdmin(admin.ModelAdmin):
	list_display = ('static_path', 'width', 'height')

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
