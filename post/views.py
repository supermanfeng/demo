from math import ceil

from django.shortcuts import render, redirect

from common.keys import POST_KEY
from post.models import Post
from post.helper import page_cache


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create.html')


def edit(request):
    if request.method == 'POST':
        # 取出 post
        post_id = int(request.POST.get('post_id', 1))
        post = Post.objects.get(id=post_id)
        # 更新数据
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id', 1))
        post = Post.objects.get(id=post_id)
        return render(request, 'edit.html', {'post': post})


@page_cache(3)
def read(request):
    post_id = int(request.GET.get('post_id', 1))
    post = Post.objects.get(id=post_id)
    return render(request, 'read.html', {'post': post})


@page_cache(1)
def post_list(request):
    page = int(request.GET.get('page', 1))
    total = Post.objects.count()
    pages = ceil(total / 5)  # 总页数

    start = (page - 1) * 5
    end = start + 5
    posts = Post.objects.all().order_by('-id')[start:end]

    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(1, pages + 1)})


def search(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, 'search.html', {'posts': posts})
