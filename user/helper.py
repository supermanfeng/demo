# coding: utf-8

from django.shortcuts import redirect, render

from user.models import User


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

            # 权限检查
            if user.has_perm(permission_name):
                return view_func(request)
            else:
                return render(request, 'blockers.html')
        return wrap2
    return wrap1
