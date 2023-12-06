from django import template
import math
register =template.Library()

@register.simple_tag
def discount_calculation(get_price,get_original_price):
    if get_original_price is None or get_original_price is 0:
        return get_price
    sellprice= get_price
    sellprice= get_price - (get_original_price * get_price/100)
    return math.floor(sellprice)


@register.filter(name='get_val')
def get_val(dictionary, key):
    return dictionary.get(str(key), 0)

@register.filter(name='ljust')
def ljust(value, arg):
    return range(int(arg))