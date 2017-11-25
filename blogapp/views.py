from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from blogapp.models import Post
from blogapp.named_tuples import PaginationData

NUM_POSTS_PER_PAGE = 5

# Create your views here.
@cache_page(60 * 15)
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
	})

@cache_page(60 * 15)
def post(request, title):
	return render(request, 'blogapp/view_post.html', {
		'post': Post.objects.get(url_name=title),
	})

def get_total_number_of_posts():
	return Post.objects.all().count()

def get_results_page(page, num_posts=NUM_POSTS_PER_PAGE):
	return Post.objects.all()[page * num_posts : (page + 1) * num_posts]
