from django.shortcuts import render
from django.contrib.staticfiles import finders

from blogapp.models import Post
from blogapp.named_tuples import PaginationData
from sass_processor.processor import sass_processor
from memoize import memoize

NUM_POSTS_PER_PAGE = 5

# Create your views here.
def index(request):
	page = int(request.GET.get('page', '0'))
	posts = list(get_results_page(page))
	pagination_data = PaginationData(
		total_posts=get_total_number_of_posts(),
		posts_per_page=NUM_POSTS_PER_PAGE,
		current_page=page,
	)

	return render(request, 'blogapp/list_posts.html', {
		'posts': posts,
		'pagination_data': pagination_data,
		'amp': False,
	})

def post(request, title):
	return render(request, 'blogapp/view_post.html', {
		'post': Post.objects.get(url_name=title),
		'amp': False,
		# Add /amp to the end of the URL and you have the AMP version
		'amp_url': request.path + '/amp',
	})

def amp_post(request, title):
	return render(request, 'blogapp/view_post.html', {
		'post': Post.objects.get(url_name=title),
		'amp': True,
		# Lop the /amp off the end of the URL and you have the canonical URL
		'canonical_url': '/'.join(request.path.split('/')[:-1]),
		'style_content': get_style_content(),
	})

def hitman(request):
	return render(request, 'hitman/hitman.html')

def get_total_number_of_posts():
	return Post.objects.all().count()

def get_results_page(page, num_posts=NUM_POSTS_PER_PAGE):
	return Post.objects.all()[page * num_posts : (page + 1) * num_posts]

@memoize()
def get_style_content():
	path = finders.find('scss/site.css')
	with open(path, 'r', encoding='utf-8') as f:
		return ''.join(f.readlines())
