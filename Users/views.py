from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from .forms import UserForm
from .models import Info, User


def response(code: int, data):
    return JsonResponse({
        'code': code,
        'data': data
    }, status=code)


def verify(request):
    if request.method == 'GET':  # and request.GET.get('type') == "verify":
        account = request.GET.get("account")
        password = request.GET.get("password")
        user = auth.authenticate(email=account, password=password)
        if user and user.is_staff:
            auth.login(request, user)
            return response(200, "Success")
        else:
            return response(202, "Failed")


@login_required
def profile(request):
    user = request.user
    if user.email.endswith('secoder.net'):
        user.stu_id = user.email.split('@')[0]
    return render(request, 'users/profile.html', {'user': user})


@login_required
def change_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功')
            return redirect('Users:profile')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'users/change_profile.html', context={'form': form})


def info_detail_view(request, pk):
    try:
        info = Info.objects.get(pk=pk)
    except Info.DoesNotExist:
        raise Http404('Info does not exist')

    return render(request, 'Info/info_detail.html', context={'info': info})
