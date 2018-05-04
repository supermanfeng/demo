# coding: utf-8

from django.shortcuts import redirect, render

from user.models import User
from user.models import Permission


def login_required(view_func):
    def wrap(request):
        if request.session.get('uid') is None:
            return redirect('/user/login/')
        else:
            return view_func(request)
    return wrap


def check_permission(permission_name):
    def wrap1(view_func):
        def wrap2(request):
            # 取出当前用户
            uid = request.session['uid']
            user = User.objects.get(id=uid)

            # 获取需要的权限
            need_perm = Permission.objects.get(name=permission_name)

            # 权限检查
            if user.perm.level >= need_perm.level:
                return view_func(request)
            else:
                return render(request, 'blockers.html')
        return wrap2
    return wrap1
