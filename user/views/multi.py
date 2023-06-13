from django.shortcuts import render, HttpResponse, redirect
from openpyxl.reader.excel import load_workbook
from user import models
from user.utils.pagination import Pagination

def multi_upload(request):
    file_object = request.FILES.get('excel_file')

    if file_object:
        # openpyxl 进行读取文件处理
        wb = load_workbook(file_object)
        sheet = wb.worksheets[0]

        for row in sheet.iter_rows(min_row=2):
            text = row[0].value

            exists = models.ExcelInfo.objects.filter(file_title=text).exists()
            if not exists:
                models.ExcelInfo.objects.create(file_title=text)

        return redirect("/document/list/")

    return redirect("/document/list/")


def multi_list(request):
    # 搜索
    # 通过url传参数搜索查询功能实现
    data_dict = {}
    search_data = request.GET.get('query', '')
    if search_data:
        data_dict['file_title__contains'] = search_data
    queryset = models.UserInfo.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'multi_list.html', context)


def multi_add(request):
    pass
