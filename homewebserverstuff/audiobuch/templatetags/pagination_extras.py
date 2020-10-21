from django import template

register = template.Library()


@register.simple_tag
def replace_add_get_key_value(request, key, new_value):
    request_cp = request.GET.copy()
    request_cp[key] = new_value

    return f"?{request_cp.urlencode()}"