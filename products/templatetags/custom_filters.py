from django import template

register = template.Library()

@register.filter(name='get_item_count')
def get_item_count(cart, product_id):
    return cart.get(product_id, 0)