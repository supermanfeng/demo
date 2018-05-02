# coding: utf-8

from django.core.cache import cache

from common import rds
from common.keys import PAGE_KEY, READ_COUNT_KEY


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