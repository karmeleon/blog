from django import template

register = template.Library()

@register.inclusion_tag('blogapp/triangle_square.html')
def render_triangle_square():
	return {
		'squares_per_side': range(3),
	}
