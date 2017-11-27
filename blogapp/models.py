import os
import frontmatter
import re
import markdown
import sys
from lxml import etree
from django.db import models
from PIL import Image as PILImage
from pyquery import PyQuery as pq

POST_PATH = 'blogapp/posts'
IMG_PATH = 'blogapp/static/img'
RASTER_FILE_ENDINGS = ('png', 'jpg', 'jpeg', 'ico')

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

class Image(models.Model):
	static_path = models.CharField(max_length=128, primary_key=True)
	width = models.IntegerField()
	height = models.IntegerField()

	@classmethod
	def normalize_path(cls, path):
		# replace \ with / to ease development on Windows platforms
		return path.replace('\\', '/')
	
	@classmethod
	def is_raster_format(cls, path):
		for ending in RASTER_FILE_ENDINGS:
			if path.endswith(ending):
				return True
		return False

	@classmethod
	def get_svg_size(cls, path):
		s = etree.parse(path).getroot()
		return s.attrib['width'], s.attrib['height']

	@classmethod
	def from_file(cls, path):
		normalized_path = cls.normalize_path(path)
		# figure out what the static path is
		# remove the IMG_PATH part
		unprefixed_path = normalized_path.replace(IMG_PATH, '')
		static_path = '/static/img' + unprefixed_path
		# get dimensions
		if cls.is_raster_format(normalized_path):
			# PIL can handle raster graphics no problem
			with PILImage.open(normalized_path) as img:
				width, height = img.size
		elif normalized_path.endswith('svg'):
			# PIL can't handle SVGs, but PyQuery can!
			width, height = cls.get_svg_size(normalized_path)
		else:
			# we found some weird file, skip it
			print(f'Couldn\'t understand ${normalized_path} as an image file, skipping', file=sys.stderr)
			return None

		return cls(
			static_path=static_path,
			width=width,
			height=height,
		)
