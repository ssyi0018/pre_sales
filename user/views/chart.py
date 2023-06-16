from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from user import models
from user.utils.bootstrap import BootStrapModelForm
import collections


class ChartModelForm(BootStrapModelForm):
    class Meta:
        model = models.ExcelInfo
        fields = ['issue_analysis', 'test_strategy']


def chart_list(request):
    return render(request, 'chart_list.html')


def chart_bar(request):
    # 获取字段信息和legend
    fields = models.ExcelInfo._meta.fields
    legend = []
    for field in fields:
        if field.attname == 'issue_analysis' or field.attname == 'test_strategy':
            legend.append(field.verbose_name)

    # 获取issue_analysis和对应的出现次数,过滤掉null值
    issue_analysis_values = models.ExcelInfo.objects.exclude(issue_analysis__isnull=True,
                                                             issue_analysis='').values_list(
        'issue_analysis', flat=True).distinct()
    issue_analysis_values = [x for x in issue_analysis_values if x is not None]
    issue_analysis_count = {value: models.ExcelInfo.objects.filter(issue_analysis=value).count()
                            for value in issue_analysis_values}

    # 获取test_strategy和对应的出现次数,过滤掉null值
    test_strategy_values = models.ExcelInfo.objects.exclude(test_strategy__isnull=True, test_strategy='').values_list(
        'test_strategy', flat=True).distinct()
    test_strategy_values = [x for x in test_strategy_values if x is not None]
    test_strategy_count = {value: models.ExcelInfo.objects.filter(test_strategy=value).count()
                           for value in test_strategy_values}

    # 构建图表数据
    date_list = list(set(list(issue_analysis_count.keys()) + list(test_strategy_count.keys())))
    series_list = []
    for name in legend:
        data = []
        for date in date_list:
            # count = issue_analysis_count.get(date, 0) if name == legend[1] else test_strategy_count.get(date, 0)
            count_dict = {}
            if len(legend) > 0 and name == legend[0]:
                count_dict = issue_analysis_count
            elif len(legend) > 1 and name == legend[1]:
                count_dict = test_strategy_count
            count = count_dict.get(date, 0)
            data.append(count)
        series_list.append({
            "name": name,
            "type": 'bar',
            "data": data
        })

    # 构建返回结果
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'date_list': date_list,
        }
    }
    # 把值传到前端
    return JsonResponse(result)
