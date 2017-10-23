from django import template

register = template.Library()

@register.inclusion_tag('blogapp/post.html')
def render_post(post):
	return {
		'post': post,
		'is_preview': False,
	}

@register.inclusion_tag('blogapp/post.html')
def render_preview(post):
	return {
		'post': post,
		'is_preview': True,
	}