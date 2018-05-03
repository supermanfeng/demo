from math import ceil

from django.shortcuts import render, redirect

from common.keys import POST_KEY, READ_COUNT_KEY
from user.helper import login_required
from post.models import Post
from post.helper import page_cache
from post.helper import read_count
from post.helper import get_top_n


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        uid = request.session['uid']
        post = Post.objects.create(uid=uid, title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, 'create.html')


@login_required
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


@read_count
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


def top10(request):
    '''
    排名 文章名                 阅读量
    1   "The Zen of Python-32"  1000
    2   "The Zen of Python-13"  900
    3   "The Zen of Python-34"  879
    4   "The Zen of Python-1"   767
    5   "The Zen of Python-9"   646
    6   "The Zen of Python-6"   432
    7   "The Zen of Python-22"  321
    8   "The Zen of Python-17"  121
    9   "The Zen of Python-31"  90
    10  "The Zen of Python-21"  71
    '''
    post_rank = get_top_n(10)
    return render(request, 'top10.html', {'rank_data': post_rank})

