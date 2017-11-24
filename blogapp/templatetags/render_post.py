from django import template

register = template.Library()

@register.inclusion_tag('blogapp/post.html')
def render_post(post):
	return {
		'post': post,
		'is_preview': False,
	}
