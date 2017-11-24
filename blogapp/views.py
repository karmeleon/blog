import os
import datetime
import time
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from blogapp.models import Post

import frontmatter

# Create your views here.
@cache_page(60 * 15)
def index(request):
	recent_posts = list(get_recent_posts(10))
	return render(request, 'blogapp/list_posts.html', {
		'posts': recent_posts
	})

@cache_page(60 * 15)
def post(request, title):
	return render(request, 'blogapp/view_post.html', {
		'post': Post.objects.get(url_name=title),
	})

def get_recent_posts(num_posts):
	return Post.objects.all()[:num_posts]
