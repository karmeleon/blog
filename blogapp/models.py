import os
import frontmatter
import re
import markdown
from pyquery import PyQuery as pq
from django.db import models

POST_PATH = 'blogapp/posts'

class Post(models.Model):
	date = models.DateField()
	filename = models.CharField(max_length=128, primary_key=True)
	title = models.CharField(max_length=256)
	preview = models.TextField()
	content = models.TextField()
	url_name = models.CharField(max_length=128)
	featured_image = models.CharField(max_length=384, default='')
	description = models.CharField(max_length=160)

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
			
			# Find the first image on the page
			m = re.search('!\[.*?\]\((.*?)\)', post.content)
			if m is not None:
				featured_image_url = 'https://sha.wn.zone' + m.group(1)
			else:
				featured_image_url = ''
			
			# We'll use the first few sentences of the first <p> tag
			# in the rendered markdown as the description for OG and JSON-LD
			markup = markdown.markdown(post_dict['preview'], extensions=[
				'markdown.extensions.tables',
				'markdown.extensions.codehilite',
				'markdown.extensions.footnotes',
			])

			p = pq(markup)
			# Images are put in <p>s, so if one has an image in it, ignore it
			eligible_paras = p('p').filter(lambda i: len(pq(this).find('img')) == 0)
			description = eligible_paras.eq(0).text()

			return cls(
				date=post_dict['date'],
				filename=filename,
				title=post_dict['title'],
				preview=post_dict['preview'],
				content=post_dict['content'],
				url_name='-'.join(os.path.splitext(filename)[0].split('-')[3:]),
				featured_image=featured_image_url,
				description=description,
			)
	
	@property
	def url(self):
		return '/p/' + self.url_name
