from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

import markdown
from pyquery import PyQuery as pq
from blogapp.models import Image

register = template.Library()

def image_size(img_src):
	img = Image.objects.get(static_path=img_src)
	return str(img.width), str(img.height)

def amplify(html):
	# Transform the given HTML to be AMP-compliant
	h = pq(html)
	# convert <img> to <amp-img>
	imgs = h('img')
	for img in imgs.items():
		# Per the W3C's HTML specification, the tag name is read-only.
		# We have to manually construct a new amp-img.
		amp_img = h('<amp-img />')
		amp_img.attr('src', img.attr('src'))
		amp_img.attr('alt', img.attr('alt'))
		# auto stretches/shrinks the image to fit the aspect ratio
		amp_img.attr('layout', 'responsive')
		# Read the image file to get its size
		width, height = image_size(img.attr('src'))
		amp_img.attr('width', width)
		amp_img.attr('height', height)
		# AMP will slurp up any other sibling elements of amp-img elements, so quarantine it
		amp_img.wrap('<div></div>')
		# Replace the old <img> with the new <amp-img>
		img.replaceWith(amp_img)
	return h.html()

@register.simple_tag(takes_context=True)
def markdownify(context, text):
	html = markdown.markdown(text, extensions=[
		'markdown.extensions.tables',
		'markdown.extensions.codehilite',
		'markdown.extensions.footnotes',
	])

	# If we're in AMP mode, we have to do some conversions.
	if context.get('amp', False):
		html = amplify(html)
	
	# Return whatever we end up with
	return mark_safe(html)