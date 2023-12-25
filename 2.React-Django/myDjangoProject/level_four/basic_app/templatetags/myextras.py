from django import template

register =  template.Library()


@register.filter(name='cutout')
def cut(value,arg):

    return value.replace(arg,'')

#register.filter('cutout',cut)


