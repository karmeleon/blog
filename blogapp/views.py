import os
import datetime
import time
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page

import frontmatter

POST_PATH = 'blogapp/posts'

# Create your views here.
@cache_page(60 * 15)
def index(request):
	recent_posts = get_recent_posts(10)
	return render(request, 'blogapp/list_posts.html', {
		'posts': recent_posts
	})

@cache_page(60 * 15)
def post(request, title):
	post = cache.get(title)
	if not post:
		# cache miss, we don't know what title this maps to (did someone hit
		# a post page right after the server fired up?), so cache all pages
		get_recent_posts(99999999)
	post = cache.get(title)
	return render(request, 'blogapp/view_post.html', {
		'post': post,
	})

def get_recent_posts(num_posts):
	posts = []
	for filename in os.listdir(POST_PATH):
		# read the date from the file
		name_parts = filename.split('-')
		date_str = '-'.join(name_parts[:3])
		post_time = datetime.datetime.strptime(date_str, '%Y-%m-%d')
		posts.append((post_time, filename))

	posts.sort(reverse=True)
	recent_posts = [read_post(*post) for post in posts[:num_posts]]
	return recent_posts
		
def read_post(date, filename):
	post_url_name = get_post_url_name(filename)
	cached_post_dict = cache.get(post_url_name)
	if cached_post_dict:
		return cached_post_dict

	# cache miss, generate the post from the file
	post = frontmatter.load(os.path.join(POST_PATH, filename))
	post_dict = post.to_dict()
	post_dict['date'] = date
	post_dict['url'] = '/p/' + get_post_url_name(filename)
	# Stuff before the "<!--more-->" is the preview
	preview_cutoff = post.content.find('<!--more-->')
	if preview_cutoff != -1:
		post_dict['preview'] = post.content[:preview_cutoff]
	else:
		# if the post is short enough, it won't have a preview
		# so just paste the entire post there.
		post_dict['preview'] = post.content
	
	# Posts are immutable as far as we care, so they live in cache forever
	cache.set(post_url_name, post_dict, None)
	
	return post_dict

def get_post_url_name(filename):
	return '-'.join(os.path.splitext(filename)[0].split('-')[3:])