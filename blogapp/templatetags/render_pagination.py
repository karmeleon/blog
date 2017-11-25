import math
from django import template

register = template.Library()

@register.inclusion_tag('blogapp/pagination.html')
def render_pagination(pagination_data):
	env = {
		'page_range': range(math.ceil(pagination_data.total_posts / pagination_data.posts_per_page)),
		'last_page': math.floor(pagination_data.total_posts / pagination_data.posts_per_page),
	}
	env.update(pagination_data._asdict())
	return env
