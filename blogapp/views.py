import os
import time
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

import frontmatter

POST_PATH = 'blogapp/posts'

# Create your views here.
def index(request):
	recent_posts = get_recent_posts(10)
	pprint(recent_posts)
	return render(request, 'blogapp/list_posts.html', {
		'posts': recent_posts
	})

def get_recent_posts(num_posts):
	posts = []
	for filename in os.listdir(POST_PATH):
		# read the date from the file
		name_parts = filename.split('-')
		date_str = '-'.join(name_parts[:3])
		post_time = time.strptime(date_str, '%Y-%m-%d')
		posts.append((post_time, filename))
	posts.sort(key=lambda x: time.mktime(x[0]))
	return [read_post(post[1]) for post in posts]
		
def read_post(filename):
	post = frontmatter.load(os.path.join(POST_PATH, filename))
	post_dict = dict(post)
	post_dict['content'] = post.content
	return post_dict
