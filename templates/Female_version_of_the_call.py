#_author:无言宝宝
#date:  2019/12/23

#用母版需要调用的函数
from django import template
register = template.Library()

@register.filter(name='addsb')
def add_sb(arg):
    return "{} sb".format(arg)


