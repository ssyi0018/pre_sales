"""用户列表，增删改查"""
from django.shortcuts import render, redirect
from django import forms
from user import models
from user.utils.pagination import Pagination
from user.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError
from user.utils.encrypt import md5


class UserForm(BootStrapModelForm):
    # 非数据库定义的字段
    confirm_password = forms.CharField(label='确认密码',
                                       widget=forms.PasswordInput(render_value=True),
                                       )

    class Meta:
        model = models.UserInfo
        fields = ['username', 'fullname', 'password', 'confirm_password', 'email', 'create_time', 'gender', 'depart',
                  'role', ]
        # fields = list(models.UserInfo._meta.get_fields()) + ['confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        MIN_PASSWORD_LENGTH = 6
        pwd = self.cleaned_data.get('password')
        if len(pwd) < MIN_PASSWORD_LENGTH:
            raise forms.ValidationError("密码长度至少为 %d 位" % MIN_PASSWORD_LENGTH)
        return md5(pwd)

    # 钩子函数,针对fields里字段
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError('密码不一致，请重新输入')
        # 返回到cleand_data里，再保存sava数据库
        return confirm


class UserInfoEditForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['username', 'fullname', 'email', 'depart']


class UserInfoResetForm(BootStrapModelForm):
    # 非数据库定义的字段
    confirm_password = forms.CharField(label='确认密码',
                                       widget=forms.PasswordInput(render_value=True),
                                       )

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        MIN_PASSWORD_LENGTH = 6
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        # 数据库校验密码是否一致
        exists = models.UserInfo.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('密码不能与之前一样！')
        elif len(pwd) < MIN_PASSWORD_LENGTH:
            raise forms.ValidationError("密码长度至少为 %d 位" % MIN_PASSWORD_LENGTH)
        return md5_pwd

    # 钩子函数,针对fields里字段
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        # pwd = self.clean_password()
        if not pwd:
            return None
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError('密码不一致，请重新输入')
        # 返回到cleand_data里，再保存sava数据库
        return confirm


def userinfo_list(request):
    # 搜索
    # 通过url传参数搜索查询功能实现
    data_dict = {}
    search_data = request.GET.get('query', '')
    if search_data:
        data_dict['username__contains'] = search_data
    queryset = models.UserInfo.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'userinfo_list.html', context)


def userinfo_add(request):
    title = '新建用户'
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'add_public.html', {'form': form, 'title': title})
    # POST进行提交后校验
    form = UserForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data) # 获取验证通过的所有数据，字典值
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, 'add_public.html', {'form': form, 'title': title})


def userinfo_edit(request, nid):
    # 获取对象
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在！'})
        # return redirect("/user/list/")
    title = '编辑用户'
    # 如果新增和删除使用一个form，可以用UserForm，如果不一样用userInfoEditForm
    if request.method == 'GET':
        form = UserInfoEditForm(instance=row_object)  # instance设置默认值
        return render(request, 'add_public.html', {'form': form, 'title': title})

    form = UserInfoEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # print(form.cleaned_data) # 获取验证通过的所有数据，字典值
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, 'add_public.html', {'form': form, 'title': title})


def userinfo_del(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def userinfo_reset(request, nid):
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在！'})

    title = '重置密码 - {}'.format(row_object.username)
    # 提交
    if request.method == 'GET':
        form = UserInfoResetForm()
        return render(request, 'add_public.html', {'form': form, 'title': title})
    form = UserInfoResetForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # print(form.cleaned_data) # 获取验证通过的所有数据，字典值
        form.save()
        return redirect("/user/list/")
    else:
        return render(request, 'add_public.html', {'form': form, 'title': title})
