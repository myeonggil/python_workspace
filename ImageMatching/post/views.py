import json
from django.contrib import messages
from django import template
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Comment, Post, Like, Tag, Learning_Result, Google_Result, Photo_Labeling
from .forms import CommentForm, PostForm, ResultForm
import learning.retrain_run_interface as inception
import learning.imagenet_example as classification
import os
import shutil
import random
import pymysql
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ast
import urllib.request as image_down
from learning.google_tensor import google_learning
import math
import operator
from media import image_path_ad

def post_list(request, tag=None):
    tag_all = Tag.objects.annotate(num_post=Count('post')).order_by('-num_post')

    if tag:
        post_list = Post.objects.filter(tag_set__name__iexact=tag) \
            .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                              'author__profile__follower_user', 'author__profile__follower_user__from_user') \
            .select_related('author__profile')
    else:
        post_list = Post.objects.all() \
            .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                              'author__profile__follower_user', 'author__profile__follower_user__from_user', ) \
            .select_related('author__profile', )

    comment_form = CommentForm()

    conn = pymysql.connect(host='localhost', user='djangouser', password='djangopass',
                           db='django_mysql', charset='utf8')

    curs = conn.cursor()

    paginator = Paginator(post_list, 2)
    page_num = request.POST.get('page')

    image_path = []
    slide_image = []
    image_len = [0, 1, 2, 3, 4, 5]
    image_brand = []
    image_name = []

    name = ''
    remember = ''

    image_info = {'name': [], 'photo': [], 'price': [], 'color': [], 'size': [], 'brand': [], 'site': []}

    sql = """select name, brand from post_link where photo like %s"""
    label_sql = """select post_id, post_label from post_photo_labeling where post_id=%s"""

    first_len = os.listdir('Images/use_images/train')
    for i in range(0, 6):
        path = 'Images/use_images/train/'
        first_index = random.randint(0, 8)
        path += first_len[first_index]
        second_len = os.listdir(path)
        second_index = random.randint(0, len(second_len) - 1)
        path += '/' + second_len[second_index]
        path = '/static/' + path.split('/')[-2] + '/' + path.split('/')[-1]
        image_path.append(path)


    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            flag = 0
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            # post.tag_save()
            label = ''
            label, result = inception.run_inference_on_image('./media/' + str(post.photo))
            sql = """insert into post_photo_labeling(post_id, post_label) values(%s, %s)"""
            curs.execute(sql, (str(post.id), str(label)))
            conn.commit()

            save_path = './media/post/' + str(request.user)
            if os.path.exists(save_path) == False:
                os.mkdir(save_path)
            save_path += '/' + str(post.id)
            google_img_path = save_path + str(request.user)
            os.mkdir(save_path)
            os.mkdir(google_img_path)

            for i in result:
                upload_path = '../../media/post/' + str(request.user) + '/' + str(post.id) + '/' + i.split('/')[-1]
                learning = Learning_Result(result_img=upload_path)
                shutil.copy(i, save_path)
                learning.author_id = str(post.author_id)
                learning.user_id = str(post.id)
                learning.save()
                flag = 1

            post.content = classification.run_inference_on_image('./media/' + str(post.photo))
            post.save()

            messages.info(request, '새 이미지가 등록되었습니다.')

            # return redirect('post:post_list')

    else:
        form = PostForm()   # post가 등록되지 않은 메인 화면

        first_len = os.listdir('Images/use_images/train')
        for i in range(0, 6):
            path = 'Images/use_images/train/'
            first_index = random.randint(0, 8)
            path += first_len[first_index]
            second_len = os.listdir(path)
            second_index = random.randint(0, len(second_len) - 1)
            path += '/' + second_len[second_index]
            path = '/static/' + path.split('/')[-2] + '/' + path.split('/')[-1]
            curs.execute(sql, '%' + path.split('/')[-1])
            rows = curs.fetchone()
            image_name.append(rows[0])
            image_brand.append(rows[1])
            image_info['name'].append(rows[0])
            image_info['brand'].append(rows[1])
            image_info['photo'].append(path)

    sql = """select name, photo, price, color, size, brand, site from post_link where photo like %s"""
    google_sql = """select google_img, google_src from post_google_result where user_id=%s"""
    try:
        result_img = {}
        result_info = {}
        google_image_src_dict = {}
        google_image_dict = {}
        name = {}
        label = {}
        posts = paginator.page(1)
        for user_id in posts:
            post_id = user_id.id
            columns = Learning_Result.objects.values_list('result_img', flat=True).filter(user_id=post_id)
            result_img['%d' % post_id] = []
            result_info['%d' % post_id] = []
            google_image_src_dict['%d' % post_id] = []
            index_out = 0
            google_image_dict['%d' % post_id] = []
            name[post_id] = user_id.content
            for column in columns:
                curs.execute(sql, '%' + column.split('/')[-1])
                rows = curs.fetchall()
                for row in rows:
                    if index_out < 6:
                        result_info['%d' % post_id].append(row)
                    else:
                        google_image_src_dict['%d' % post_id].append(row)

                    # name[post_id] = row[1].split('/')[-2]

                if index_out < 6:
                    result_img['%d' % post_id].append(str(column))
                else:
                    google_image_dict['%d' % post_id].append(str(column))

                index_out += 1

            curs.execute(label_sql, (str(post_id)))
            row = curs.fetchone()
            label[row[0]] = row[1]

            """curs.execute(google_sql, (str(post_id)))
            rows = curs.fetchall()
            google_image_dict['%d' % post_id] = []
            google_image_src_dict['%d' % post_id] = []
            for row in rows:
                google_image_src_dict['%d' % post_id].append(row[0])
                google_image_dict['%d' % post_id].append(row[1])"""



    except PageNotAnInteger:
        result_img = {}
        result_info = {}
        google_image_src_dict = {}
        google_image_dict = {}
        name = {}
        label = {}
        posts = paginator.page(1)
        for user_id in posts:
            post_id = user_id.id
            columns = Learning_Result.objects.values_list('result_img', flat=True).filter(user_id=post_id)
            result_img['%d' % post_id] = []
            result_info['%d' % post_id] = []
            google_image_src_dict['%d' % post_id] = []
            index_out = 0
            google_image_dict['%d' % post_id] = []
            name[post_id] = user_id.content
            for column in columns:
                curs.execute(sql, '%' + column.split('/')[-1])
                rows = curs.fetchall()
                for row in rows:
                    if index_out < 6:
                        result_info['%d' % post_id].append(row)
                    else:
                        google_image_src_dict['%d' % post_id].append(row)


                if index_out < 6:
                    result_img['%d' % post_id].append(str(column))
                else:
                    google_image_dict['%d' % post_id].append(str(column))

                index_out += 1

            curs.execute(label_sql, (str(post_id)))
            row = curs.fetchone()
            label[row[0]] = row[1]
            """curs.execute(google_sql, (str(post_id)))
            rows = curs.fetchall()
            google_image_dict['%d' % post_id] = []
            google_image_src_dict['%d' % post_id] = []
            for row in rows:
                google_image_src_dict['%d' % post_id].append(row[0])
                google_image_dict['%d' % post_id].append(row[1])"""

    except EmptyPage:
        result_img = {}
        result_info = {}
        google_image_src_dict = {}
        google_image_dict = {}
        name = {}
        label = {}
        posts = paginator.page(1)
        for user_id in posts:
            post_id = user_id.id
            columns = Learning_Result.objects.values_list('result_img', flat=True).filter(user_id=post_id)
            result_img['%d' % post_id] = []
            result_info['%d' % post_id] = []
            google_image_src_dict['%d' % post_id] = []
            index_out = 0
            google_image_dict['%d' % post_id] = []
            name[post_id] = user_id.content
            for column in columns:
                curs.execute(sql, '%' + column.split('/')[-1])
                rows = curs.fetchall()
                for row in rows:
                    if index_out < 6:
                        result_info['%d' % post_id].append(row)
                    else:
                        google_image_src_dict['%d' % post_id].append(row)

                if index_out < 6:
                    result_img['%d' % post_id].append(str(column))
                else:
                    google_image_dict['%d' % post_id].append(str(column))

                index_out += 1

            curs.execute(label_sql, (str(post_id)))
            row = curs.fetchone()
            label[row[0]] = row[1]
            """curs.execute(google_sql, (str(post_id)))
            rows = curs.fetchall()
            google_image_dict['%d' % post_id] = []
            google_image_src_dict['%d' % post_id] = []
            for row in rows:
                google_image_src_dict['%d' % post_id].append(row[0])
                google_image_dict['%d' % post_id].append(row[1])"""


    if request.is_ajax():  # Ajax request 여부 확인
        return render(request, 'post/post_list_ajax.html', {
            'posts': posts,
            'comment_form': comment_form,
        })

    """if request.method == 'POST':
        tag = request.POST.get('tag')
        tag_clean = ''.join(e for e in tag if e.isalnum())  # 특수문자 삭제
        return redirect('post:post_search', tag_clean)"""

    return render(request, 'post/post_list.html', {
        'tag': tag,
        'posts': posts,
        'name': name,
        'comment_form': comment_form,
        'tag_all': tag_all,
        'result_imgs': result_img,
        'image_path': image_path,
        'image_len': image_len,
        'image_name': image_name,
        'image_brand': image_brand,
        'image_info': image_info,
        'result_info': result_info,
        'form': form,
        'google_imgs': google_image_dict,
        'google_info': google_image_src_dict,
        'labels': label,
    })

def my_post_list(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    user_profile = user.profile

    target_user = get_user_model().objects.filter(id=user.id).select_related('profile') \
        .prefetch_related('profile__follower_user__from_user', 'profile__follow_user__to_user')

    post_list = user.post_set.all()

    return render(request, 'post/my_post_list.html', {
        'user_profile': user_profile,
        'target_user': target_user,
        'post_list': post_list,
        'username': username,
    })


def my_post_list_detail(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    user_profile = user.profile

    target_user = get_user_model().objects.filter(id=user.id).select_related('profile') \
        .prefetch_related('profile__follower_user__from_user', 'profile__follow_user__to_user')

    post_list = Post.objects.filter(author=user) \
        .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                          'author__profile__follower_user', 'author__profile__follower_user__from_user', ) \
        .select_related('author__profile', )

    comment_form = CommentForm()

    paginator = Paginator(post_list, 3)
    page_num = request.POST.get('page')

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.is_ajax():  # Ajax request 여부 확인
        return render(request, 'post/post_list_ajax.html', {
            'posts': posts,
            'comment_form': comment_form,
        })

    return render(request, 'post/my_post_list_detail.html', {
        'user_profile': user_profile,
        'username': username,
        'posts': posts,
        'comment_form': comment_form,
        'target_user': target_user,
    })

def follow_list(request, username):
    pass


@login_required
def follow_post_list(request):
    follow_set = request.user.profile.get_following
    post_list = Post.objects.filter(author__profile__in=follow_set) \
        .prefetch_related('tag_set', 'like_user_set__profile', 'comment_set__author__profile',
                          'author__profile__follower_user', 'author__profile__follower_user__from_user', ) \
        .select_related('author__profile', )

    comment_form = CommentForm()

    paginator = Paginator(post_list, 3)
    page_num = request.POST.get('page')

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.is_ajax():  # Ajax request 여부 확인
        return render(request, 'post/post_list_ajax.html', {
            'posts': posts,
            'comment_form': comment_form,
        })

    return render(request, 'post/post_list.html', {
        'follow_set': follow_set,
        'posts': posts,
        'comment_form': comment_form,
    })


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_save()
            result = inception.run_inference_on_image('./media/' + str(post.photo))

            save_path = './media/post/' + str(request.user)
            if os.path.exists(save_path) == False:
                os.mkdir(save_path)
            save_path += '/' + str(post.id)
            os.mkdir(save_path)

            for i in result:
                upload_path = '../../media/post/' + str(request.user) + '/' + str(post.id) + '/' + i.split('/')[-1]
                learning = Learning_Result(result_img=upload_path)
                shutil.copy(i, save_path)
                learning.author_id = str(post.author_id)
                learning.user_id = str(post.id)
                learning.save()

            messages.info(request, '새 사진이 등록되었습니다.')

            return redirect('post:post_list')

    else:
        form = PostForm()
    return render(request, 'post/post_new.html', {
        'form': form,
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.tag_set.clear()  # NOTE: ManyToManyField 의 모든 항목 삭제 (해당 인스턴스 내에서만 적용)
            post.tag_save()
            messages.success(request, '수정완료')
            return redirect('post:post_list')

    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {
        'post': post,
        'form': form,
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    learning = Learning_Result.objects.filter(user_id=post.id)
    google = Google_Result.objects.filter(user_id=post.id)
    labels = Photo_Labeling.objects.filter(post_id=post.id)
    post_id = post.id

    if post.author != request.user or request.method == 'GET':
        messages.warning(request, '잘못된 접근입니다.')
        return redirect('post:post_list')

    if request.method == 'POST':
        learning.delete()
        post.delete()
        google.delete()
        labels.delete()
        os.remove('./media/' + str(post.photo))
        images = os.listdir('./media/post/' + str(request.user) + '/' + str(post_id))
        google_images = os.listdir('./media/post/' + str(request.user) + '/' + str(post_id) + str(request.user))
        for i in images:
            os.remove('./media/post/' + str(request.user) + '/' + str(post_id) + '/' + i)
        for i in google_images:
            os.remove('./media/post/' + str(request.user) + '/' + str(post_id) + str(request.user) + '/' + i)
        os.rmdir('./media/post/' + str(request.user) + '/' + str(post_id))
        os.rmdir('./media/post/' + str(request.user) + '/' + str(post_id) + str(request.user))

        messages.success(request, '삭제완료')

        return redirect('post:post_list')


@login_required
@require_POST  # 해당 뷰는 POST method 만 받는다.
def post_like(request):
    pk = request.POST.get('pk', None)
    post = get_object_or_404(Post, pk=pk)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:
        post_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': post.like_count,
               'message': message,
               'nickname': request.user.profile.nickname}

    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def comment_new(request):
    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return render(request, 'post/comment_new_ajax.html', {
                'comment': comment,
            })
    return redirect("post:post_list")


@login_required
def comment_delete(request):
    pk = request.POST.get('pk')
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
        message = '삭제완료'
        status = 1

    else:
        message = '잘못된 접근입니다.'
        status = 0

    return HttpResponse(json.dumps({'message': message, 'status': status, }), content_type="application/json")


def comment_more(request):
    pk = request.POST.get('pk')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comments = post.comment_set.all()[4:]
        return render(request, 'post/comment_more_ajax.html', {
            'comments': comments,
        })
    return redirect("post:post_list")
