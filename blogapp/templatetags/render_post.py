from django import template

register = template.Library()

@register.inclusion_tag('blogapp/post.html', takes_context=True)
def render_post(context, post):
	return {
		'post': post,
		'is_preview': False,
		'amp': context['amp'],
	}
