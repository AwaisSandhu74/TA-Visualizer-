from django import template
register = template.Library()

@register.filter
def get_index(h,i):
    try:
        value = h[i]
    except:
        value = -1
    
    return value