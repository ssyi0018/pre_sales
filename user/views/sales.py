import json
import os
from user import models
from urllib.parse import unquote
from django.conf import settings
from django.http import FileResponse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.utils.bootstrap import BootStrapModelForm
from user.utils.pagination import Pagination


class SalesModelForm(BootStrapModelForm):
    # # 移除样式
    # bootstrap_exclude_fields = ['filepath']
    class Meta:
        model = models.SalesInfo
        # fields = '__all__'
        # 排除某个字段
        exclude = ['filename', 'create_time', 'user', 'sort_id', ]


def sales_list(request):
    # 查询
    search_data = request.GET.get('query', '')
    if search_data:
        queryset = models.SalesInfo.objects.filter(filename__contains=search_data).order_by('-id')
    else:
        queryset = models.SalesInfo.objects.all().order_by('-id')
    # 左边菜单查询
    sort = request.GET.get('sort', '')
    if sort:
        queryset = queryset.filter(sort=sort)
        return render(request, 'sales_list_table.html', {'queryset': queryset})
    page_object = Pagination(request, queryset, page_size=5)
    form = SalesModelForm()
    context = {'form': form,
               'queryset': page_object.page_queryset,
               'page_string': page_object.html(),
               'search_data': search_data,
               }
    return render(request, 'sales_list.html', context)


@csrf_exempt
def sales_add(request):
    form = SalesModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # file_name = request.FILES['filepath'].name.split('.')[0]
        # file_ext = request.FILES['filepath'].name.split('.')[-1]
        # if file_ext == 'pptx' or file_ext == 'ppt':
        #     form.instance.filepath.name = request.FILES['filepath'].name
        # 非页面上提交的字段
        form.instance.update_time = timezone.now()
        # 获取account里登陆的session中id
        form.instance.user_id = request.session['info']['id']
        # 文件名重复判断
        filename = request.FILES['filepath'].name
        if models.SalesInfo.objects.filter(filename=filename).exists():
            return JsonResponse({'status': False, 'filename_exists': True})
        form.instance.filename = filename
        form.save()
        # 返回到Ajax里res
        # 下面两句意思相等
        return JsonResponse({'status': True})
    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


@csrf_exempt
def sales_edit(request):
    uid = request.GET.get('uid')
    row_object = models.SalesInfo.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '数据不存在，请刷新重试！'})

    form = SalesModelForm(data=request.POST, instance=row_object, files=request.FILES)
    if form.is_valid():
        row = form.save(commit=False)
        if 'filepath' in request.FILES:
            row.filename = request.FILES['filepath'].name
        row.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def sales_detail(request):
    # 方式一
    uid = request.GET.get('uid')
    # 方式一
    # row_object = models.Order.objects.filter(id=uid).first()
    # 方式二，数据库获得字典
    row_dict = models.SalesInfo.objects.filter(id=uid).values('filename', 'sort', 'renew').first()
    if not dict:
        return JsonResponse({'status': False, 'error': '数据不存在！'})
    result = {
        'status': True,
        'data': row_dict,
    }
    # 给前端res数据
    return JsonResponse(result)


def sales_delete(request):
    uid = request.GET.get('uid')
    exists = models.SalesInfo.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在！'})
    models.SalesInfo.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})
