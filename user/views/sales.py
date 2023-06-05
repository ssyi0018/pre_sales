import json
from user import models
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
        exclude = ['filename', 'create_time', 'user', ]


def sales_list(request):
    # 查询
    data_dict = {}
    search_data = request.GET.get('query', '')
    if search_data:
        data_dict['filename__contains'] = search_data

    queryset = models.SalesInfo.objects.all().order_by('-id')
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
    # title = 'ModelForm上传'
    # if request.method == 'GET':
    #     form = SalesModelForm()
    #     return render(request, 'sales_add.html', {'form': form, 'title': title})
    form = SalesModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        file_name = request.FILES['filepath'].name.split('.')[0]
        file_ext = request.FILES['filepath'].name.split('.')[-1]
        if file_ext == 'pptx' or file_ext == 'ppt':
            form.instance.filepath.name = request.FILES['filepath'].name
        # 非页面上提交的字段
        form.instance.update_time = timezone.now().strftime('%Y-%m-%d-%H:%M:%S')
        # 获取account里登陆的session中id
        form.instance.user_id = request.session['info']['id']
        form.instance.filename = file_name
        form.save()
        # 返回到Ajax里res
        # 下面两句意思相等
        return JsonResponse({'status': True})
    data_dict = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
