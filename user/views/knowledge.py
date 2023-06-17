from django.shortcuts import render, HttpResponse


def knowledge_list(request):
    return render(request, 'knowledge_list.html')
