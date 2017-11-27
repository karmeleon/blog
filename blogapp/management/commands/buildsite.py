import os
from django.core.management.base import BaseCommand
from django.db.models import Q
from blogapp.models import Post, Image, POST_PATH, IMG_PATH

class Command(BaseCommand):
	help = 'Reads all posts and images and inserts/modifies/deletes rows from the DB to reflect it.'

	def handle(self, *args, **options):
		# Get all the filenames in POST_PATH
		post_filenames = os.listdir(POST_PATH)
		# Delete all the posts in the DB whose filenames don't exist in the posts directory
		Post.objects.filter(~Q(filename__in=post_filenames)).delete()
		# Add/update all posts in the posts directory
		for filename in post_filenames:
			post = Post.from_file(filename).save()
		
		# Now do static images
		existing_files = []
		for root, dirs, files in os.walk(IMG_PATH):
			for name in files:
				image = Image.from_file(os.path.join(root, name))
				# this can be None if the file isn't an image file
				if image is not None:
					image.save()
					existing_files.append(image.static_path)
		
		# Delete all the images in the DB whose filenames don't exist in the img directory
		Image.objects.filter(~Q(static_path__in=existing_files)).delete()

