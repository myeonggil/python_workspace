from django import template
import re
import os
from django.utils.safestring import mark_safe
import json
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ast
import urllib.request as image_down
from learning.load_tensor import learning

register = template.Library()

@register.filter
def add_link(value):
    content = value.content
    tags = value.tag_set.all()
    for tag in tags:
        content = re.sub(r'\#'+tag.name+r'\b', '<a href="/post/explore/tags/'+tag.name+'">#'+tag.name+'</a>', content)
    return content

@register.filter
def list_index(list, index):
    return list[index]

@register.filter
def string_to_integer(variable):
    return int(variable)

@register.filter
def counter_info(id, b):
    return id, b

@register.filter
def name_init(id, result_info):
    return result_info['%s' % id[0]][id[1]][0]

@register.filter
def photo_init(id, result_info):
    return result_info['%s' % id[0]][id[1]][1]

@register.filter
def price_init(id, result_info):
    return result_info['%s' % id[0]][id[1]][2]

@register.filter
def color_init(id, result_info):
    color_list = ''
    temp = ''
    if result_info['%s' % id[0]][id[1]][5] == 'tiag':
        temp = result_info['%s' % id[0]][id[1]][3].split('\n')
        for i in temp:
            color_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'rakun':
        temp = result_info['%s' % id[0]][id[1]][3].split('\n')
        for i in temp:
            color_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'dj2':
        temp = result_info['%s' % id[0]][id[1]][3]
        for i in temp:
            color_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'vintage':
        temp = result_info['%s' % id[0]][id[1]][3]
        for i in temp:
            color_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'alondon':
        temp = result_info['%s' % id[0]][id[1]][4].split('\n')
        for i in temp:
            color_list += i

    return color_list

@register.filter
def size_init(id, result_info):
    size_list = ''
    if result_info['%s' % id[0]][id[1]][5] == 'tiag':
        temp = result_info['%s' % id[0]][id[1]][4].split('\n')
        for i in temp:
            size_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'rakun':
        temp = result_info['%s' % id[0]][id[1]][4].split('\n')
        for i in temp:
            size_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'dj2':
        temp = result_info['%s' % id[0]][id[1]][4]
        for i in temp:
            size_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'vintage':
        temp = result_info['%s' % id[0]][id[1]][4]
        for i in temp:
            size_list += i
    elif result_info['%s' % id[0]][id[1]][5] == 'alondon':
        temp = result_info['%s' % id[0]][id[1]][4].split('\n')
        for i in temp:
            size_list += i

    return size_list

@register.filter
def brand_init(id, result_info):
    return result_info['%s' % id[0]][id[1]][5]

@register.filter
def site_init(id, result_info):
    return result_info['%s' % id[0]][id[1]][6]

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter
def image_class(row, column):
    name = row[column]
    return name

@register.filter
def label_class(labels, post_id):
    label = labels[post_id]
    return label

@register.filter
def google(dictionary, post_id):
    src_list = dictionary[post_id]
    return src_list

@register.filter
def google_href(diction, count):
    href = diction[count]
    return href
