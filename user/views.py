from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from user.models import User
from user.forms import RegisterForm
from user.helper import login_required
from user.helper import check_permission


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)  # 密码做一次哈希处理
            user.save()

            # 记录用户登录状态
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname', '').strip()
        password = request.POST.get('password', '').strip()
        # 验证密码
        try:
            user = User.objects.get(nickname=nickname)
            if check_password(password, user.password):
                # 记录用户登录状态
                request.session['uid'] = user.id
                request.session['nickname'] = user.nickname
                return redirect('/user/info/')
            else:
                return render(request, 'login.html', {'error': '密码错误'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': '用户不存在'})
    return render(request, 'login.html', {})


@login_required
def user_info(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user': user})


@login_required
def logout(request):
    request.session.flush()
    return redirect('/user/login/')


@check_permission('admin')
def del_user(request):
    need_delete_user_id = request.GET.get('user_id')
    need_delete_user = User.objects.get(id=need_delete_user_id)
    need_delete_user.delete()
