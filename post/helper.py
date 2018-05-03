# coding: utf-8

from django.core.cache import cache

from common import rds
from common.keys import PAGE_KEY, READ_COUNT_KEY
from post.models import Post


def page_cache(timeout):
    '''
    缓存更新的策略
        1. 手动更新
        2. 删除旧缓存
        3. 通过过期时间自动更新
    '''
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            key = PAGE_KEY % request.get_full_path()
            response = cache.get(key)
            print('get response from cache:', response)
            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(key, response, timeout)
                print('set response from view:', response)
            return response
        return wrap2
    return wrap1


def read_count(read_view):
    def wrap(request):
        post_id = int(request.GET.get('post_id', 1))
        rds.zincrby(READ_COUNT_KEY, post_id)
        return read_view(request)
    return wrap


def get_top_n(count):
    ori_data = rds.zrevrange(READ_COUNT_KEY, 0, count - 1, withscores=True)
    # [(b'34', 17.0),        [[34, 17],
    #  (b'12', 10.0),         [12, 10],
    #  (b'2', 9.0),           [ 2,  9],
    #  (b'1', 9.0),    =>     [ 1,  9],
    #  (b'20', 8.0),          [20,  8],
    #  (b'38', 6.0),          [38,  6],
    #  (b'35', 3.0)]          [35,  3]]
    rank_data = [[int(post_id), int(count)] for post_id, count in ori_data]
    post_id_list = [post_id for post_id, _ in rank_data]  # 取出 post_id 列表

    # 方法 1
    # # post_dict = {1: <Post: Post object>,
    # #              2: <Post: Post object>,
    # #              12: <Post: Post object>,
    # #              ...}
    # post_dict = Post.objects.in_bulk(post_id_list)
    # post_rank = [[post_dict[pid], count] for pid, count in rank_data]

    # 方法 2
    posts = Post.objects.filter(id__in=post_id_list)
    posts = sorted(posts, key=lambda post: post_id_list.index(post.id))
    post_rank = [[post, rank[1]] for post, rank in zip(posts, rank_data)]

    return post_rank
