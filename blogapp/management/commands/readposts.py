import os
from django.core.management.base import BaseCommand
from django.db.models import Q
from blogapp.models import Post, POST_PATH

class Command(BaseCommand):
	help = 'Reads all polls in blogapp/posts and inserts/updates/deletes them in the database as necessary.'

	def handle(self, *args, **options):
		# Get all the filenames in POST_PATH
		filenames = os.listdir(POST_PATH)
		# Delete all the posts in the DB whose filenames don't exist in the posts directory
		Post.objects.filter(~Q(filename__in=filenames)).delete()
		# Add/update all posts in the posts directory
		for filename in filenames:
			post = Post.from_file(filename).save()
