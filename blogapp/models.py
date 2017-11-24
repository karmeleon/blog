import os
import frontmatter
import hashlib
from django.db import models

POST_PATH = 'blogapp/posts'

class Post(models.Model):
	date = models.DateField()
	filename = models.CharField(max_length=128, primary_key=True)
	title = models.CharField(max_length=256)
	preview = models.TextField()
	content = models.TextField()
	file_hash = models.CharField(max_length=64)
	url_name = models.CharField(max_length=128)

	class Meta:
		ordering = ['-date']

	@classmethod
	def from_file(cls, filename):
		"""Builds a Post from a file.
		"""
		with open(os.path.join(POST_PATH, filename), 'r', encoding='utf-8') as f:
			text = ''.join(f.readlines())
			post = frontmatter.loads(text)
			post_dict = post.to_dict()
			# Stuff before the "<!--more-->" is the preview
			preview_cutoff = post.content.find('<!--more-->')
			if preview_cutoff != -1:
				post_dict['preview'] = post.content[:preview_cutoff]
			else:
				# if the post is short enough, it won't have a preview
				# so just paste the entire post there.
				post_dict['preview'] = post.content
			
			return cls(
				date=post_dict['date'],
				filename=filename,
				title=post_dict['title'],
				preview=post_dict['preview'],
				content=post_dict['content'],
				file_hash=hashlib.sha256(text.encode()).hexdigest(),
				url_name='-'.join(os.path.splitext(filename)[0].split('-')[3:]),
			)
	
	@property
	def url(self):
		return '/p/' + self.url_name
