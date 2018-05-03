# coding: utf-8

'''
访问次数       时间戳
      1  10000000.00
      2  10000000.31
      3  10000001.09

      4  10000001.32
      5  10000001.33

      6  10000001.32
'''

import time

from django.utils.deprecation import MiddlewareMixin


class BlockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        now = time.time()
        request_time = request.session.get('request_time', [0, 0])
        if (now - request_time[0]) < 1:
            time.sleep(100)
        request.session['request_time'] = [request_time[1], time.time()]
